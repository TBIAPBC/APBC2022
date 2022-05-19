import copy
import random
import sys
import traceback
import multiprocessing
import threading
import queue
import time

from Game.game_utils import nameFromPlayerId
from Game.game_utils import Direction, MoveStatus
from Game.game_utils import Tile, TileStatus, TileObject
from Game.game_utils import Map, Status, GameParameters

from Game.illustrator import Illustrator

class Simulator(object):
	def __init__(self, *, map, seed=None, vizfile=None, framerate):
		self.rng = random.Random()
		if seed is None:
			seed = random.randrange(sys.maxsize)
		self.rng.seed(seed)
		self.seed = seed
		self.map = map = copy.deepcopy(map)
		for x in range(map.width):
			for y in range(map.height):
				if map[x, y].status == TileStatus.Unknown:
					raise ValueError("Tile (%d, %d) is unkown." % (x, y))
				map[x, y].obj = None

		self.printInitial = True
		self.printRoundBegin = True
		self.printEvents = True
		self.printMoves = True
		self._debugMoves = False
		self._debugPlayerCrash = False

		self.params = GameParameters()

		self._players = []
		self._goldPots = goldPots = {}  # (x, y) -> int
		for i in range(self.params.maxNumGoldPots):
			self._add_gold_pot()

		self.goldPotRemainingRounds = self.params.goldPotTimeOut

		# keep a dictionary of the mines
		self._mines = {}  # (x, y) -> expiry_round -- the round in which the mine should expire

		self._status = status = []  # the internal data, without map
		self._pubStat = pubStat = []  # the object we give the player each time, updated from the internal data

		self.illustrator = Illustrator(self.map, vizfile, framerate)

	def _random_empty_spot(self):
		while True:
			x = self.rng.randint(0, self.map.width - 1)
			y = self.rng.randint(0, self.map.height - 1)
			if self.map[x, y].status != TileStatus.Empty:
				continue
			if self.map[x, y].obj is not None:
				continue
			break
		return (x,y)

	def add_player(self, p):
		pId = len(self._players)
		self._players.append(p)
		(x,y) = self._random_empty_spot()
		self.map[x, y].obj = TileObject.makePlayer(pId)
		self._status.append(Status(pId, x=x , y=y, health=self.params.maxHealth,
					   gold=self.params.initialGoldPerPlayer))
		self._pubStat.append(Status(pId, x=x, y=y, health=self.params.maxHealth,
					    gold=self.params.initialGoldPerPlayer, params=self.params))

		# duplicate the public status object in the player object
		p.status = self._pubStat[-1]

	def play(self, *, rounds):
		rounds = int(rounds)
		for pId in range(len(self._players)):
			# to avoid breaking the player interface,
			# set number of rounds in the players status objects
			self._pubStat[pId].params.rounds=rounds

			self._players[pId].reset(pId, len(self._players), self.map.width, self.map.height)

		self.illustrator._add_robots(self._players)
		self.illustrator._add_nrounds(rounds)

		if self.printInitial:
			print("Initial board:")
			print(self)

		for r in range(1, rounds + 1):
			self._begin_round(r)
			self._handle_shooting(r)
			self._handle_setting_mines(r)
			self._handle_moving(r)
			self._handle_healing(r)
			# TODO: something to do at the end of the round?
			self.illustrator.append_goldpots(self._goldPots)
			self.illustrator.append_robots(self._players)
			self.illustrator.append_mines(getattr(self,'_mines',{}))

		print("=" * 80)
		print("Final board:")
		print(self)
		if self.illustrator.vizfile:
			self.illustrator._illustrate()


	# relocate gold pot(s)
	def _empty_and_relocate_gold_pots(self):
		for coord, amount in self._goldPots.items():
			print("Gold pot at ({:>3}, {:>3}) with {} coints emtpied and relocated\n".
			      format(coord[0], coord[1], amount))
			self.map[coord].obj = None

		self._goldPots = {}
		for i in range(self.params.maxNumGoldPots):
			self._add_gold_pot()
		self.goldPotRemainingRounds = self.params.goldPotTimeOut

	def _begin_round(self, r):
		# remove expired mines
		for xy,expirydate in list(self._mines.items()):
			if expirydate <= r:
				# remove the mine
				del self._mines[xy]
				self.map[xy] = Tile(TileStatus.Empty)
				print("Remove expired mine at %s." % (str(xy)) )

		# relocate gold pots if timed out
		self.goldPotRemainingRounds -=1
		if self.goldPotRemainingRounds <= 0:
			self._empty_and_relocate_gold_pots()


		# add gold and health to each player
		for pId in range(len(self._players)):
			s = self._status[pId]
			s.gold += self.params.goldPerRound
			self._increase_health(pId, self.params.healthPerRound)

		for pId in range(len(self._players)):
			s = self._status[pId]
			pub = self._pubStat[pId]
			self._copy_to_public(s, pub)

		# reset the task counter
		self._tasksThisRound = [0 for pId in self._players]

		if self.printRoundBegin:
			# https://stackoverflow.com/questions/2084508/clear-terminal-in-python
			#print(chr(27) + "[2J")
			print("=" * 80)
			print("Round %d:" % r)
			print(self)
		for p in self._players:
			p.round_begin(r)

	def _increase_health(self, pId, amount):
		self._status[pId].health = min(self.params.maxHealth, self._status[pId].health + amount)

	def _decrease_health(self, pId, amount):
		self._status[pId].health = max(0, self._status[pId].health - amount)

	def _pay_for_task(self, pId):
		# returns whether it could be payed for or not
		s = self._status[pId]
		cost = 1 + self._tasksThisRound[pId]
		if s.gold < cost:
			return False
		s.gold -= cost
		self._tasksThisRound[pId] += 1
		for pos in self._goldPots:
			if self.params.goldDecrease and self.goldPotRemainingRounds <= self.params.goldDecreaseTime:
				self._goldPots[pos] -= 1
			else:
				self._goldPots[pos] += 1
		return True

	def _handle_shooting(self, r):
		# TODO
		pass

	def _handle_setting_mines(self, r):
		# just go through players and set their mines - rules are
		# sufficiently simple, to handle player one-by-one
		for pId in range(len(self._players)):
			player = self._players[pId]
			pstatus = player.status
			player_coords = (pstatus.x, pstatus.y)

			# first, ask the player whether and where to set mines
			try:
				mines = list(self._players[pId].set_mines(self._pubStat[pId]))

				# check that the answer is in correct
				# format
				for (x,y) in mines:
					if not (isinstance(x,int) and
						isinstance(y,int)):
						raise TypeError("Player's set mines must return list of coordinates")
					# catch out of bounds -- errors invalidate the entire action
					if x<0 or x>=self.map.width or y<0 or y>=self.map.height:
						raise ValueError("Mine coordinates not on the map")

			except NotImplementedError as e:
			    	# if not implemented, simply pass w/o
				# making some fuzz about it
				mines = []
				pass
			except Exception as e:
				print("ERROR: player %d raised an exception: %s" % (pId, str(e)))
				traceback.print_exc(file=sys.stdout)
				mines = []

			# place mines and charge the player
			for xy in mines:
				paid=True
				d = self._distance(player_coords, xy)
				for i in range(d):
					paid = self._pay_for_task(pId)
					if not paid: break
				if paid:
					# set the mine
					# if it is legal to place it (otherwise ignore, but still charge!)
					if not self.map[xy].is_blocked() and self.map[xy].obj is None:
						self._mines[xy] = r + self.params.mineExpiryTime
						self.map[xy] = Tile(TileStatus.Mine)
						print("Player %s sets mine at %s (distance %d; expires in round %d)."
							% (str(pId), str(xy), d, self._mines[xy]) )
				else:
					break # don't even try to set more mines

	def _askPlayerForMoves(self,pId):
		try:
			q = multiprocessing.Queue()

			def ask():
				q.put( list(self._players[pId].move(self._pubStat[pId])) )

			p = multiprocessing.Process(target=ask())
			p.start()
			moves = q.get(timeout = self.params.moveTimeout)

			# check that the answer is in correct
			# format
			for m in moves:
				if not isinstance(m, Direction):
					raise TypeError("Players must return moves as list of directions")
		except queue.Empty as e:
			print("ERROR: player %d didn't answer in time." % (pId))
			moves = []
		except Exception as e:
			print("ERROR: player %d raised an exception: %s" % (pId, str(e)))
			traceback.print_exc(file=sys.stdout)
			moves = []

		if p.is_alive():
			p.terminate()
		p.join()
		return moves

	# @param r round index
	def _handle_moving(self, r):
		numPlayers = len(self._players)
		movesPerPlayer = []  # from the user
		moveStatusPerPlayer = []  # should be given to the user

		#movesPerPlayer = [ self._askPlayerForMoves(pId) for pId in range(numPlayers) ]

		print("Ask players for moves...")
		q = queue.Queue()
		def askPlayer(pId,startTime):
			moves = self._askPlayerForMoves(pId)
			q.put( (pId, moves) )
			print("Player {} returns moves after {:3.1f}s: {}"
				.format( pId, time.time()-startTime,
			                 list(map(str,moves)) ))

		threads = [ threading.Thread( target=askPlayer, args=(pId,time.time()) ) for pId in range(numPlayers) ]
		for t in threads: t.start()
		for t in threads: t.join()

		movesPerPlayer = [None] * len(self._players)
		while not q.empty():
			(pId, moves) = q.get()
			movesPerPlayer[pId] = moves

		for moves in movesPerPlayer:
			mStatus = [MoveStatus.Pending for m in moves]
			moveStatusPerPlayer.append(mStatus)
			if self._debugMoves:
				print("Debug: %s; [%s]" % (nameFromPlayerId(pId), ", ".join(str(m) for m in moves)))

		def cancelRest(pId, mId):
			for i in range(mId + 1, len(movesPerPlayer[pId])):
				moveStatusPerPlayer[pId][i] = MoveStatus.Cancelled

		# do a move for each player in lock-step
		maxNumMoves = max(len(ms) for ms in movesPerPlayer)
		for mId in range(maxNumMoves):
			# collect all pairs of positions,
			# and evaluate if the player is actually allowed to move
			moves = [None for p in self._players]
			for pId in range(len(self._players)):
				now = self._status[pId].x, self._status[pId].y
				then = now
				moves[pId] = (now, then)
				# first, this player may actually have no more moves
				if mId >= len(movesPerPlayer[pId]):
					continue
				# a player must _always_ pay for a move, even though it is not carried out
				paid = self._pay_for_task(pId)
				# a previous move in this round could have cancelled this move
				if moveStatusPerPlayer[pId][mId] == MoveStatus.Cancelled:
					continue
				assert moveStatusPerPlayer[pId][mId] == MoveStatus.Pending

				# if we can't pay, don't move, and cancel everything afterwards
				if not paid:
					moveStatusPerPlayer[pId][mId] = MoveStatus.OutOfGold
					cancelRest(pId, mId)
					continue

				# if we are too weak then we can't move either
				if self._status[pId].health < self.params.minMoveHealth:
					moveStatusPerPlayer[pId][mId] = MoveStatus.OutOfHealth
					print("Player",pId,"is too weak to move")
					continue

				# otherwise, actually try to move
				moveStatusPerPlayer[pId][mId] = MoveStatus.Done
				diff = movesPerPlayer[pId][mId].as_xy()
				then = now[0] + diff[0], now[1] + diff[1]
				moves[pId] = (now, then)
			# check collisions
			# - with walls or the boundary
			for pId in range(len(moves)):
				if mId >= len(movesPerPlayer[pId]):
					continue
				ms = moveStatusPerPlayer[pId][mId]
				if ms != MoveStatus.Done:
					continue
				dest = moves[pId][1]
				if (
					   dest[0] < 0 or dest[0] >= self.map.width
					or dest[1] < 0 or dest[1] >= self.map.height
					or self.map[dest].status != TileStatus.Empty
					):
					moveStatusPerPlayer[pId][mId] = MoveStatus.CrashWall
					cancelRest(pId, mId)
					moves[pId] = moves[pId][0], moves[pId][0]

			# identify crashs
			#   - 1) two or more players move to the same position;
			#	 this includes that one of the players does not move
			#   - 2) two players swap positions (crossing paths)
			#   crashs change the moving behavior -> we need to calculate a fix point

			while True:
				# check crash of type (1)
				targets=dict()
				for pId,p in enumerate(self._players):
					dest = moves[pId][1]
					if not dest in targets:
						targets[dest] = list()
					targets[dest].append(pId)

				crashed=set()
				for t in targets:
					if len(targets[t])>1:
						#print("Crash of robots", targets[t],"at",t)
						for pId in targets[t]:
							crashed.add(pId)

				# check crash of type (2)
				for pId1,p1 in enumerate(self._players):
					for pId2,p2 in enumerate(self._players):
						if pId1==pId2: continue
						if moves[pId1] == moves[pId2][::-1]:
							#print("Crossing paths of robots",
							#      pId1,"and",pId2,"at",moves[pId1])
							crashed.add(pId1)
							crashed.add(pId2)

				for pId in crashed:
					moves[pId] = moves[pId][0],moves[pId][0]
					if mId < len(movesPerPlayer[pId]):
						moveStatusPerPlayer[pId][mId] = MoveStatus.CrashPlayer
						cancelRest(pId, mId)

				if len(crashed)>0: continue
				else: break

			# update health after crashes
			for pId in range(len(moves)):
				if mId >= len(movesPerPlayer[pId]):
					continue
				ms = moveStatusPerPlayer[pId][mId]
				if ms == MoveStatus.CrashWall:
					self._decrease_health(pId, self.params.healthPerWallCrash)
				elif ms == MoveStatus.CrashPlayer:
					self._decrease_health(pId,
								  self.params.healthPerPlayerCrash
								  + random.randint(0,self.params.healthPerPlayerCrashRandom))

			# print unsuccessful moves
			if self._debugMoves:
				print("Debug: move round %d" % mId)
				for pId in range(len(self._players)):
					print("Debug: move status %s; [%s]" % (nameFromPlayerId(pId), ", ".join(str(m) for m in moveStatusPerPlayer[pId])))
			if self.printEvents:
				for pId in range(len(moves)):
					if mId >= len(movesPerPlayer[pId]):
						continue
					ms = moveStatusPerPlayer[pId][mId]
					assert ms != MoveStatus.Pending
					if ms == MoveStatus.Done:
						continue
					mStr = str(movesPerPlayer[pId][mId])
					pStr = nameFromPlayerId(pId)
					if ms == MoveStatus.CrashWall:
						print("Event: %s crashed into a wall while trying to move %s." % (pStr, mStr))
					elif ms == MoveStatus.CrashPlayer:
						print("Event: %s crashed into another player while trying to move %s." % (pStr, mStr))
					elif ms == MoveStatus.OutOfGold:
						print("Event: %s could not move %s. No enough gold." % (pStr, mStr))
					elif ms == MoveStatus.OutOfHealth:
						print("Event: %s could not move %s. No health." % (pStr, mStr))
					elif ms == MoveStatus.Cancelled:
						print("Event: %s could not move %s due to a previous event this round." % (pStr, mStr))
					else:
						print("Bug: %s could not move due to some strange reason (debug: ms == %s)." % (pStr, str(ms)))

			# update positions
			# - first remove them
			toUpdate = []
			for pId in range(len(moves)):
				if mId >= len(movesPerPlayer[pId]):
					continue
				ms = moveStatusPerPlayer[pId][mId]
				if ms != MoveStatus.Done:
					continue
				if self.printMoves:
					print("Event:", nameFromPlayerId(pId), "moved", movesPerPlayer[pId][mId])
				toUpdate.append(pId)
				assert self.map[moves[pId][0]].obj is not None
				assert self.map[moves[pId][0]].obj.is_player(pId)
				self.map[moves[pId][0]].obj = None
			# - then add them again at new positions
			#   ... while taking gold
			numGoldPotsTaken = 0
			for pId in toUpdate:
				destObj = self.map[moves[pId][1]].obj
				if destObj is not None:
					assert destObj.is_gold()
					amount = self._goldPots[moves[pId][1]]
					if self.printEvents:
						print("Event:", nameFromPlayerId(pId), "took a pot of %d gold." % amount)
					self._status[pId].gold += amount
					del self._goldPots[moves[pId][1]]
					numGoldPotsTaken += 1
				self.map[moves[pId][1]].obj = TileObject.makePlayer(pId)
				self._status[pId].x, self._status[pId].y = moves[pId][1]
			#relocate other gold pots(starts new timer)
			if numGoldPotsTaken>0:
				if (self.params.maxNumGoldPots-numGoldPotsTaken)>0:
					self._empty_and_relocate_gold_pots()
				else:
					self.goldPotRemainingRounds = self.params.goldPotTimeOut
			for i in range(numGoldPotsTaken):
				self._add_gold_pot()

	def _handle_healing(self, r):
		# TODO
		pass

	def _copy_to_public(self, pri, pub):
		assert pri.player == pub.player
		pub.x, pub.y, pub.health, pub.gold = pri.x, pri.y, pri.health, pri.gold
		pub.map = Map(width=self.map.width, height=self.map.height)
		# copy the part that is visible
		xl = max(pri.x - self.params.visibility, 0)
		yl = max(pri.y - self.params.visibility, 0)
		xu = min(pri.x + self.params.visibility, self.map.width - 1)
		yu = min(pri.y + self.params.visibility, self.map.height - 1)
		for x in range(xl, xu + 1):
			for y in range(yl, yu + 1):
				pub.map[x, y] = copy.deepcopy(self.map[x, y])
		pub.goldPots = copy.deepcopy(self._goldPots)
		for x, y in self._goldPots:
			pub.map[x, y] = copy.deepcopy(self.map[x, y])

		pub.goldPotRemainingRounds = self.goldPotRemainingRounds

		# make information about other visible players available
		pub.others = list()
		for status in self._status:
			pubStatus = None
			if (status.player != pub.player
				and xl <= status.x and status.x <= xu
				and yl <= status.y and status.y <= yu):
				pubStatus = copy.deepcopy(status)
			pub.others.append(pubStatus)

	@staticmethod
	def _distance(xy,xy1):
		return max(abs(xy1[0]-xy[0]),abs(xy1[1]-xy[1]))

	def _min_dist_to_player(self,xy):
		"""
		Return the minimum distance of xy to any of the players
		"""
		return min( self._distance(xy, (self._status[pId].x,self._status[pId].y))
			    for pId in range(len(self._players)) )

	def _add_gold_pot(self):
		# find a spot nicely remote from the robots
		if len(self._players)>0:
			(x,y) = max( [ self._random_empty_spot() for i in range(7) ],
					 key=lambda xy: self._min_dist_to_player(xy) )
		else:
			(x,y) = self._random_empty_spot()

		self.map[x, y].obj = TileObject.makeGold()
		self._goldPots[x, y] = self.params.initialGoldPotAmount

	def __str__(self):
		s = str(self.map)
		s += "Player   Health   Gold      Position\n"
		for i in range(len(self._players)):
			s += "{:<9}{:<9}{:<9} {},{}\n".format(nameFromPlayerId(i), self._status[i].health, self._status[i].gold, self._status[i].x, self._status[i].y)
		s += "Gold Pots:\n"
		for coord, amount in self._goldPots.items():
			s += "Gold pot, ({:>3}, {:>3}): {} ({})\n".format(coord[0], coord[1],
									  amount,
									  self.goldPotRemainingRounds)
		return s
