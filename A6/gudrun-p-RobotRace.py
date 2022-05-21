# -*- coding: utf-8 -*-
"""
Created on Tue May 17 12:57:35 2022

@author: Gudrun Poetzelberger, 00275117
"""

from game_utils import nameFromPlayerId
from game_utils import Direction as D, MoveStatus
from game_utils import Tile, TileStatus, TileObject
from game_utils import Map, Status
from simulator import Simulator
from gudrun_p_player_base import Player
from gudrun_p_shortestpaths import AllShortestPaths
import time  # sleep before print to avoid caching issues


## Future Ideas:
## Later: I might implement a check if the treasure is too far away, and just wait in this case.
## Later: Out of all the shortest paths, I could choose it such that unknown fields are twice as "long" as 
## known empty fields (since there might be walls i dont know about, these fields are not as "good" as 
## known empty fields)
## Later: if path to gold has no unknown tiles, calculate if it might be worth it to walk all the way in one round
## Later: if otherPlayer in similar distance to gold, then go faster?

## Robot Idea: Robot who mostly waits and only goes to gold if it is very close and enemies are not close



class FastPlayer(Player):
	
	#def __init__(self):
	#	print("init called")
	#	self.atest = 0  # TODO : delete (this is for debugging. atest keeps being reset?? -> solved: ask() in simulator multithreading)
	
	def reset(self, player_id, max_players, width, height):
		self.printDebugMessages = True  # set to true to get a lot of print statements from this robot
		self.player_name = "goGetter" # nameFromPlayerId(player_id)
		self.player_id = player_id
		self.rememberedMap = Map(width, height)  # locally saved map that will remember all Tiles we have already seen
		self.minFractionOfGoldToKeep = 0.2  # try to not spend more than 0.8 of your remaining gold in one round
		self.safetyFraction = 0.5 # Weight for if it is "worth it" to go after the amount of gold in the goldPot.
		## Should be between 0 and 1. The smaller the fraction, the fewer moves the robot makes.
		#self.atest = 0 # TODO delete
		
	
	def round_begin(self, r):
		self._debugMessage("RBegin " + str(r) + ". I am player " + str(self.player_id) + ".")
		#pass
	
	
	def move(self, status):
		#self._debugMessage("old atest = " + str(self.atest))
		#self.atest = self.atest + 1
		#self._debugMessage("new atest = " + str(self.atest))
		#self._debugMessage("OLD remembered Map:\n" + str(self.rememberedMap))
		# the status object (see game_utils.Status) contains:
		# - .player, our id, if we should have forgotten it
		# - .x and .y, our position
		# - .health and .gold, how much health and gold we have
		# - .map, a map of what we can see (see game_utils.Map)
		#   The origin of the map is in the lower left corner.
		# - .goldPots, a dict from positions to amounts
		# - (? .params all the GameParamenters?)
		# - (?.params.goldPotRemainingRounds, how many rounds the gold pot(s) still has left before being removed?)
		# print("-" * 80)

		try:

			# -- print the map as we can see it, along with health and gold: --
			#self._debugMessage("\n" + str(status))
			#print("Status for %s" % self.player_name)
			#print(status)

			# -- update the map that the robot saves with information from the server: --
			#self.rememberedMap = self.rememberedMap
			for x in range(self.rememberedMap.width):
				for y in range(self.rememberedMap.height):
					if status.map[x, y].status != TileStatus.Unknown:  # map[x,y].status is an enum: Unknown, Empty, Wall, Mine
						self.rememberedMap[x, y].status = status.map[x, y].status
					if status.map[x, y].obj is not None:
						self.rememberedMap[x, y].obj = status.map[x, y].obj
					else:
						self.rememberedMap[x, y].obj = None

			self._debugMessage("Remembered Map:\n" + str(self.rememberedMap))


			#strategy:
			## Pretend all unknown fields are empty. Calculate shortest path to gold under this assumption.
			## Walk along this path as far as it is within the visible portion of the map.
			## I call this the lavish strategy because the robot is just throwing around money and is not stingy.


			# -- Do not move if you are too weak to move (that would only waste money since you still pay) --
			if status.health < status.params.minMoveHealth:
				self._debugMessage("Health is too low to move so no movements sent.")
				return list()

			# -- Set some useful variables: --
			currentPosition = (status.x,status.y)
			assert len(status.goldPots) > 0
			goldCoords = next(iter(status.goldPots))  # the dictionary status.goldPots ( (x,y) -> amount) has
			## only one entry. Iter iterates over the keys (coordinates), but here I only have 1 pair of coordinates.
			goldInPot = list(status.goldPots.values())[0]  # so this is a list with only one entry (?), and the entry is the amount of gold.

			# -- calculate desired path: --
			paths = AllShortestPaths(goldCoords, self.rememberedMap)
			chosenPath = paths.shortestPathFrom(currentPosition)  # TODO : maybe smartly choose among the shortest paths.
			chosenPath = chosenPath[1:]  # (I think this is because we calculate the path from the gold to the
			chosenPath.append(goldCoords)  ## player instead of the other way round)
			self._debugMessage("Gold is at: " + str(goldCoords))
			self._debugMessage("Shortest path to gold:\n" + str(chosenPath))
			chosenPath = self._movesOnKnownTiles(status, chosenPath)
			self._debugMessage("Part of shortest path that is on known tiles: " + str(chosenPath))

			# -- check that I dont run into other players: --
			chosenPath = self._avoidPlayerCollisions(chosenPath)
			if chosenPath == []:
				self._debugMessage("There is another player blocking the path. No movements sent.")
				return []

			# -- check if the gold reward is worth it: --
			numberOfMoves = len(chosenPath)
			costOfMoves = self._costOfMoves(numberOfMoves)
			if costOfMoves >= goldInPot:
				self._debugMessage("Path on known Tiles would cost " + str(costOfMoves) + " gold, but the reward is only " + str(goldInPot) + " gold. Therefore I reduce the number of moves.")
				chosenPath = self._reduceMoveAmount(chosenPath, chosenPath, goldInPot)

			# -- do try not to spend ALL your money: --
			minFractionOfGoldToKeep = self.minFractionOfGoldToKeep  # used only if goldpot is not reached in THIS ROUND
			if chosenPath[-1] != goldCoords:
				self._debugMessage("Gold will not be reached in this round.")
				chosenPath = self._saveSomeGold(chosenPath, minFractionOfGoldToKeep, status)

			maxMoves = 1000 # TODO : delete this

			# TODO : take into account rounds that gold will still be on map

			# -- send moves to simulator: --
			if maxMoves < len(chosenPath):
				self._debugMessage("Path I buy: " + str(chosenPath[:maxMoves]) + "\n = " + str(self._as_directions(currentPosition, chosenPath[:maxMoves])))
				return self._as_directions(currentPosition, chosenPath[:maxMoves])
			else:
				self._debugMessage("Path I buy: " + str(chosenPath) + "\n = " + str(self._as_directions(currentPosition, chosenPath)))
				return self._as_directions(currentPosition, chosenPath)
		except Exception as e:
			self._debugMessage("Exception: " + str(e))
			#print(e)
			return []
		


	# ----- Helper Functions: -----
	
	def _as_direction(self,curpos,nextpos):
		#print("curpos = ", curpos)
		#print("nextpos = ", nextpos)
		for d in D:
			diff = d.as_xy()
			#print("for d = ", d, "aka diff = ", diff)
			#print("curpos[0] + diff[0], curpos[1] + diff[1] = " , curpos[0] + diff[0], curpos[1] + diff[1])
			if (curpos[0] + diff[0], curpos[1] + diff[1]) ==  nextpos:
				return d
		return None

	def _as_directions(self,curpos,path):
		# (zip: list of tuples, in this case tuples of tuples ((x1, y1),(x2, y2)), ((x2,y2),(x3,y3)), ... ?)
		return [self._as_direction(x,y) for x,y in zip([curpos]+path,path)]
	
	
	def _movesOnKnownTiles(self, status, coordinatePath):
		knownPath = list()
		for eachCoord in coordinatePath:
			if self.rememberedMap[eachCoord].status != TileStatus.Unknown:
				knownPath.append(eachCoord)
			else:
				return knownPath  # as soon as the first Unknown Tile interrupts the path, stop the function.
		return knownPath  # return list of (x,y) tuples that are the first few coordinates of the shortest path.
	
	def _costOfMoves(self, numMoves):
		# Gauss summation of all numbers 0 to numMoves:
		cost = (numMoves + 1) * numMoves/2.0
		return cost

	def _reduceMoveAmount(self, wholePath, knownPath, goldInPot):
		path = list()
		if len(knownPath) >= goldInPot:  # reaching gold is always a loss
			self._debugMessage("The Gold is too far away. I will wait.")
			return path
		else:
			i = 0
			while self._costOfMoves(len(path)) < goldInPot * self.safetyFraction and i < len(knownPath):
				path.append(knownPath[i])
				i = i+1
			return path
	
	def _saveSomeGold(self, path, fraction, status):
		newPath = list()
		i = 0
		while i < len(path) and status.gold - self._costOfMoves(len(newPath)+1) >= status.gold * 0.2:  # len + 1 because then I append
			newPath.append(path[i])
			i = i + 1
		self._debugMessage("_saveSomeGold: new path is " + str(newPath)) #TODO delete
		return newPath

	def _avoidPlayerCollisions(self, oldPath):
		newPath = list()
		for coords in oldPath:
			if self.rememberedMap[coords].obj is None:  # empty fields can be one the path
				newPath.append(coords)
			elif self.rememberedMap[coords].obj.is_player():
				if self.rememberedMap[coords].obj.is_player(self.player_id):  # my own player is not an obstacle
					newPath.append(coords)
				else :  # other players should not be appended to path
					self._debugMessage("There is another player in my way: Player " + str(self.rememberedMap[coords].obj) + " is at coordinates " + str(coords))
					return newPath
			else: # non-empty fields with no players on them, i.e. gold
				newPath.append(coords)
		return newPath



	def _debugMessage(self, message):
		if self.printDebugMessages:
			time.sleep(0.00000001)
			print(self.player_name, ": ", message)
			


# --------------------------------------------------------------------------



class WaitingPlayer(Player):
	
	def reset(self, player_id, max_players, width, height):
		self.player_name = "waitingWalter" # nameFromPlayerId(player_id)
		self.player_id = player_id
		self.rememberedMap = Map(width, height)  # locally saved map that will remember all Tiles we have already seen
		self.printDebugMessages = True # set to true to get a lot of print statements from this robot
	
	def round_begin(self, r):
		self._debugMessage("RBegin " + str(r) + ". I am player " + str(self.player_id) + ".")
		pass
	
	
	def move(self, status):
		self.maxGoldDistance = status.params.visibility  # change this to a lower number to move less often
		## cannot set this earlier since I need status to do it (if I want the value to be visibility)
		
		# -- print the map as we can see it, along with health and gold: --
		self._debugMessage("\n" + str(status))
		
		# -- update the map that the robot saves with information from the server: --
		rememberedMap = self.rememberedMap
		for x in range(rememberedMap.width):
			for y in range(rememberedMap.height):
				if status.map[x, y].status != TileStatus.Unknown:  # map[x,y].status is an enum: Unknown, Empty, Wall, Mine
					rememberedMap[x, y].status = status.map[x, y].status
		
		
		
		# strategy: 
		## Wait until gold is close Robot. Then go get it. Otherwise don't move.
		## This strategy does not work very well, because the Server always puts the gold away from the player
		## So in the end this robot really just. Does Not Move. But still slowly accumulates gold!
		
		# -- Do not move if you are too weak to move (that would only waste money since you still pay) --
		if status.health < status.params.minMoveHealth:
			self._debugMessage("Health is too low to move so no movements sent.")
			return list()
		
		# -- Set some useful variables: --
		currentPosition = (status.x,status.y)
		assert len(status.goldPots) > 0
		goldCoords = next(iter(status.goldPots))
		goldInPot = list(status.goldPots.values())[0]  # so this is a list with only one entry (?), and the entry is the amount of gold.
		
		# -- if gold not within defined range, then do not move
		if self._isGoldInRange(status, goldCoords) == False:
			return list()
		
		
		# if we do want to get the gold:
		
		# -- calculate desired path: --
		paths = AllShortestPaths(goldCoords,rememberedMap)
		chosenPath = paths.shortestPathFrom(currentPosition)
		chosenPath = chosenPath[1:]  # (I think this is because we calculate the path from the gold to the 
		chosenPath.append(goldCoords)  ## player instead of the other way round)
		self._debugMessage("Gold is at: " + str(goldCoords))
		self._debugMessage("Shortest path to gold:\n" + str(chosenPath))
		
		# -- check if the gold reward is worth it: --
		numberOfMoves = len(chosenPath)
		costOfMoves = self._costOfMoves(numberOfMoves)
		if costOfMoves >= goldInPot:
			self._debugMessage("Path on known Tiles would cost " + str(costOfMoves) + " gold, but the reward is only " + str(goldInPot) + " gold. Therefore I do not move.")
			return list()
		# if gold reward is worth it, go get it:
		else:
			return self._as_directions(currentPosition, chosenPath)
		
	
	# ---- Helper Functions: ----
	
	
	def _isGoldInRange(self, status, goldCoords):
		xmin = max(0, status.x - self.maxGoldDistance)
		xmax = min(status.map.width, status.x + self.maxGoldDistance)
		ymin = max(0, status.y - self.maxGoldDistance)
		ymax = min(status.map.height, status.y + self.maxGoldDistance)
		for x in range(xmin, xmax):
			for y in range(ymin, ymax):
				if (x,y) == goldCoords:
					self._debugMessage("Gold is in range!")
					return True
		return False
	
		
		
	# -- from FastPlayer: --
	
	def _debugMessage(self, message):
		if self.printDebugMessages:
			print(self.player_name, ": ", message)
	
	def _as_direction(self,curpos,nextpos):
		#print("curpos = ", curpos)
		#print("nextpos = ", nextpos)
		for d in D:
			diff = d.as_xy()
			#print("for d = ", d, "aka diff = ", diff)
			#print("curpos[0] + diff[0], curpos[1] + diff[1] = " , curpos[0] + diff[0], curpos[1] + diff[1])
			if (curpos[0] + diff[0], curpos[1] + diff[1]) ==  nextpos:
				return d
		return None

	def _as_directions(self,curpos,path):
		# (zip: list of tuples, in this case tuples of tuples ((x1, y1),(x2, y2)), ((x2,y2),(x3,y3)), ... ?)
		return [self._as_direction(x,y) for x,y in zip([curpos]+path,path)]
	
	def _costOfMoves(self, numMoves):
		# Gauss summation of all numbers 0 to numMoves:
		cost = (numMoves + 1) * numMoves/2.0
		return cost
		
		
#players = [FastPlayer()]
#players = [WaitingPlayer()]
players = [FastPlayer(), WaitingPlayer()]