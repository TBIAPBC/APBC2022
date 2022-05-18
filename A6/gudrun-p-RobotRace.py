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
from player_base import Player
from shortestpaths import AllShortestPaths


## Future Ideas:
## Later: I might implement a check if the treasure is too far away, and just wait in this case.
## Later: Out of all the shortest paths, I could choose it such that unknown fields are twice as "long" as 
## known empty fields (since there might be walls i dont know about, these fields are not as "good" as 
## known empty fields)
## Later: if path to gold has no unknown tiles, calculate if it might be worth it to walk all the way in one round
## Later: if otherPlayer in similar distance to gold, then go faster?

## Robot Idea: Robot who mostly waits and only goes to gold if it is very close and enemies are not close



class FastPlayer(Player):
	def reset(self, player_id, max_players, width, height):
		self.player_name = "goGetter" # nameFromPlayerId(player_id) 
		self.rememberedMap = Map(width, height)  # locally saved map that will remember all Tiles we have already seen
		self.printDebugMessages = True
	
	def round_begin(self, r):
		pass
	
	
	def move(self, status):
		# the status object (see game_utils.Status) contains:
		# - .player, our id, if we should have forgotten it
		# - .x and .y, our position
		# - .health and .gold, how much health and gold we have
		# - .map, a map of what we can see (see game_utils.Map)
		#   The origin of the map is in the lower left corner.
		# - .goldPots, a dict from positions to amounts
		# - .goldPotRemainingRounds, how many rounds the gold pot(s) still has left before being removed
		# print("-" * 80)
		print("Status for %s" % self.player_name)
		# # print the map as we can see it, along with health and gold
		print(status)
		
		# update the map that the robot saves with information from the server:
		rememberedMap = self.rememberedMap
		for x in range(rememberedMap.width):
			for y in range(rememberedMap.height):
				if status.map[x, y].status != TileStatus.Unknown:  # map[x,y].status is an enum: Unknown, Empty, Wall, Mine
					rememberedMap[x, y].status = status.map[x, y].status
		
		#strategy: 
		## Pretend all unknown fields are empty. Calculate shortest path to gold under this assumption.
		## Walk along this path as far as it is within the visible portion of the map.
		## I call this the lavish strategy because the robot is just throwing around money and is not stingy.

		currentPosition = (status.x,status.y)
		assert len(status.goldPots) > 0
		goldCoords = next(iter(status.goldPots))  # the dictionary status.goldPots ( (x,y) -> amount) has 
		## only one entry. Iter iterates over the keys (coordinates), but here I only have 1 pair of coordinates.
		goldInPot = list(status.goldPots.values())[0]  # so this is a list with only one entry (?), and the entry is the amount of gold.
		
		paths = AllShortestPaths(goldCoords,rememberedMap)
		chosenPath = paths.shortestPathFrom(currentPosition)  # TODO : maybe smartly choose among the shortest paths.
		chosenPath = chosenPath[1:]  # (I think this is because we calculate the path from the gold to the 
		chosenPath.append(goldCoords)  ## player instead of the other way round)
		distance=len(chosenPath)
		self._debugMessage("Gold is at: " + str(goldCoords))
		self._debugMessage("Shortest path to gold:\n" + str(chosenPath))
		chosenPathOnKnownTiles = self._movesOnKnownTiles(status, chosenPath)
		self._debugMessage("Part of shortest path that is on known tiles: " + str(chosenPathOnKnownTiles))
		
		numberOfMoves = len(chosenPathOnKnownTiles)
		costOfMoves = self._costOfMoves(numberOfMoves)
		if costOfMoves >= goldInPot:
			self._debugMessage("Path on known Tiles would cost " + str(costOfMoves) + " gold, but the reward is only " + str(goldInPot) + " gold. Therefore I reduce the number of moves.")
			chosenPathOnKnownTiles = self._reduceMoveAmount(chosenPath, chosenPathOnKnownTiles, goldInPot)
			
		
		
		maxMoves = 100 # TODO: write function depending on gold and cost, such that e.g. only 1/4 of remainaing gold can be spent
		
		# TODO : dont move if the pot is too far away
		
		if maxMoves < len(chosenPathOnKnownTiles):
			self._debugMessage("Path I buy:\n" + str(chosenPathOnKnownTiles[:maxMoves]) + "\n = " + str(self._as_directions(currentPosition, chosenPathOnKnownTiles[:maxMoves])))
			return self._as_directions(currentPosition, chosenPathOnKnownTiles[:maxMoves])
		else:
			self._debugMessage("Path I buy:\n" + str(chosenPathOnKnownTiles) + "\n = " + str(self._as_directions(currentPosition, chosenPathOnKnownTiles)))
			return self._as_directions(currentPosition, chosenPathOnKnownTiles)
		


	# --- Helper Functions: ---
	
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
		safetyFraction = 0.5  # the smaller the fraction, the fewer moves the robot makes. If it is 1, the robot spends all the money it has.
		if len(knownPath) >= goldInPot:  # reaching gold is always a loss
			self._debugMessage("The Gold is too far away. I will wait.")
			return path
		else:
			i = 0
			while self._costOfMoves(len(path)) < goldInPot * safetyFraction:
				path.append(knownPath[i])
				i = i+1
			return path
		return path


	def _debugMessage(self, message):
		if self.printDebugMessages:
			print(self.player_name, ": ", message)

players = [FastPlayer()] # TODO rename the player