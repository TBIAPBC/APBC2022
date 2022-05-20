from enum import Enum
import random
from collections import deque
import copy


def nameFromPlayerId(i):
	assert i >= 0
	assert i <= ord("z") - ord("a") + 1
	return chr(ord("a") + i)


class Direction(Enum):
	up = 0
	down = 1
	left = 2
	right = 3
	up_left = 4
	up_right = 5
	down_left = 6
	down_right = 7

	def as_xy(self):
		return {
			self.up:         ( 0,  1),
			self.down:       ( 0, -1),
			self.left:       (-1,  0),
			self.right:      ( 1,  0),
			self.up_left:    (-1,  1),
			self.up_right:   ( 1,  1),
			self.down_left:  (-1, -1),
			self.down_right: ( 1, -1),
		}[self]

	def __str__(self):
		return {
			self.up:         "UP",
			self.down:       "DOWN",
			self.left:       "LEFT",
			self.right:      "RIGHT",
			self.up_left:    "UP LEFT",
			self.up_right:   "UP RIGHT",
			self.down_left:  "DOWN LEFT",
			self.down_right: "DOWN RIGHT",
		}[self]


class MoveStatus(Enum):
	Pending = 0
	Done = 1
	CrashWall = 2 # includes crashing into mines
	CrashPlayer = 3
	OutOfGold = 4
	OutOfHealth = 5
	Cancelled = 6  # used for any move after something went wrong

class TileStatus(Enum):
	Unknown = 0
	Empty = 1
	Wall = 2
	Mine = 3

	def is_blocked(self):
		"""
		Tiles can be blocked by either walls or mines
		"""
		return self==self.Wall or self==self.Mine
	
	@staticmethod
	def strings():
		return ["_", ".", "#"]

	@classmethod
	def unstr(cls,x):
		return cls(cls.strings().index(x))

	def __str__(self):
		return {
			self.Unknown: "_",
			self.Empty:  ".",
			self.Wall: "#",
			self.Mine: "&"
		}[self]


class TileObject(object):
	@staticmethod
	def makePlayer(i):
		assert i >= 0
		return TileObject(i)

	@staticmethod
	def makeGold():
		return TileObject(-1)

	def __init__(self, i):
		self._i = i
		assert i >= -1

	def is_gold(self):
		return self._i == -1

	def is_player(self, pId=None):
		if pId is None:
			return self._i >= 0
		else:
			return self._i == pId

	def as_player(self):
		assert self.is_player()
		return self._i

	def __str__(self):
		sym="."
		if self.is_gold():
			sym = "$"
		elif self.is_player():
			sym = chr(ord('A') + self._i)
		return '\033[91m'+'\033[1m'+sym+'\033[0m'

class Tile(object):
	def __init__(self, status, obj=None):
		if obj is not None and not isinstance(obj, TileObject):
			raise TypeError("Tile.obj must be a TileObject or None.")
		self.status = status
		self.obj = obj
		if obj is not None:
			assert not self.is_blocked()

	def is_blocked(self):
		return self.status.is_blocked()

	def __str__(self):
		if self.obj is not None:
			return str(self.obj)
		else:
			return str(self.status)


class Map(object):
	def __init__(self, width, height):
		"""Make a map full of 'unknown'."""
		self.width = int(width)
		self.height = int(height)
		assert width > 0
		assert height > 0
		self._data = []
		for y in range(height):
			row = []
			for x in range(width):
				row.append(Tile(TileStatus.Unknown))
			self._data.append(row)

	def __str__(self):
		print
		return "\n".join(" ".join(str(tile) for tile in row) for row in reversed(self._data)) + "\n"

	def __getitem__(self, coord):
		assert coord[0] >= 0
		assert coord[1] >= 0
		assert coord[0] < self.width
		assert coord[1] < self.height
		return self._data[coord[1]][coord[0]]

	def __setitem__(self, coord, val):
		assert coord[0] >= 0
		assert coord[1] >= 0
		assert coord[0] < self.width
		assert coord[1] < self.height
		self._data[coord[1]][coord[0]] = val

	@staticmethod
	def makeEmpty(width, height):
		m = Map(width, height)
		for y in range(height):
			for x in range(width):
				m._data[y][x] = Tile(TileStatus.Empty)
		return m

	# return the non-Wall (actually, non-blocked) neighbors of a field (x,y)
	def nonWallNeighbours(self,xy):
		neighbours = []
		for d in Direction:
			diff = d.as_xy()
			coord = xy[0] + diff[0], xy[1] + diff[1]
			if coord[0] < 0 or coord[0] >= self.width:
				continue
			if coord[1] < 0 or coord[1] >= self.height:
				continue
			tile = self[coord]
			if not tile.is_blocked():
				neighbours.append((d, coord))
		return neighbours

	def _find_first_if(self,testfun):
		for x in range(self.width):
			for y in range(self.height):
				if testfun(self._data[y][x]):
					return (x,y)
		return None

	def _count_if(self,testfun):
		count = 0
		for x in range(self.width):
			for y in range(self.height):
				if testfun(self._data[y][x]):
					count += 1
		return count

	def _connected(self):
		def is_empty(x): return x.status == TileStatus.Empty

		xy = self._find_first_if(is_empty)

		front = deque()
		front.append(xy)

		accessible=set()
		accessible.add(xy)

		# mark all accessible fields
		while front:
			xy=front.popleft()

			for d,neighbour in self.nonWallNeighbours(xy):
				if not neighbour in accessible:
					front.append(neighbour)
					accessible.add(neighbour)

		return len(accessible) == self._count_if(is_empty)

	@staticmethod
	def makeRandom(width, height, p):
		## assume that p is not too large; otherwise
		## resampling is very uneffective

		assert p<=0.4

		while True:
			m = Map(width, height)
			for y in range(height):
				for x in range(width):
					if random.random() < p:
						s = TileStatus.Wall
					else:
						s = TileStatus.Empty
					m._data[y][x] = Tile(s)

			if m._connected():
				return m
			#print("Resample map")
			#print(m)

	@staticmethod
	def read(filename):
		## assume that p is not too large; otherwise
		## resampling is very uneffective

		def toTile(x):
			return { '_': TileStatus.Unknown,
				 '.': TileStatus.Empty,
				 '#': TileStatus.Wall
			}[x]

		with open(filename) as fh:
			data = [ [ Tile(TileStatus.unstr(x)) for x in line.strip() ]
				 for line in fh.readlines() ]

		height = len(data)
		width=0
		if height>0: width = len(data[0])

		m = Map(width,height)
		m._data = data
		return m

 
## The game parameters
class GameParameters(object):
	def __init__(self):
		self.maxNumGoldPots = 1
		self.initialGoldPotAmount = 100
		self.initialGoldPerPlayer = 99
		self.goldPerRound = 1
		self.goldPotTimeOut = 20 # after how many rounds the pot is emptied and replaced
		self.goldDecrease = True #does the amount of gold in the pot(s) decrease after a certain time
		self.goldDecreaseTime = self.goldPotTimeOut/2; #after which time does the amount of gold in the pot(s) decrease 
		self.healthPerRound = 10
		self.minMoveHealth = 30 # minimum health that allows to move
		self.maxHealth = 100
		self.visibility = 7
		self.healthPerWallCrash = 25
		self.healthPerPlayerCrash = 15
		self.healthPerPlayerCrashRandom = 5

		self.moveTimeout = 2 # players get at most moveTimeout seconds to answer each move request

		self.mineExpiryTime = 3 # how many rounds do mines exist

		self._cost = [0]

	# the cost of actions
	def cost(self,actions):
		assert actions >= 0
		if actions >= len(self._cost):
			self._cost.append( self.cost(actions-1)+actions )
		return self._cost[actions]

class Status(object):
	def __init__(self, player, *, x, y, health, gold=0, params=None):
		self.player = player
		self.x = x
		self.y = y
		self.health = health
		self.gold = gold

		# info in the public status provided to players
		self.params = copy.deepcopy(params)

		self.map = None # limited info about map
		self.others = None # limited info about other players in the visibility range
		self.goldPots = None # dict: (x, y) -> amount

	def __str__(self):
		s="Player "+str(self.player)+"\n"
		if self.map is not None: s += str(self.map)
		s += "Health: %d\nGold:   %d\n" % (self.health, self.gold)

		if self.goldPots is not None:
			for coord, amount in self.goldPots.items():
				s += "Gold pot, ({:>3}, {:>3}): {}\n".format(coord[0], coord[1], amount)
		return s
