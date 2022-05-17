#!/usr/bin/env python3
import random

from game_utils import nameFromPlayerId
from game_utils import Direction as D, MoveStatus
from game_utils import Tile, TileStatus, TileObject
from game_utils import Map, Status
from simulator import Simulator
from player_base import Player

class MyRandomPlayer(Player):
	def reset(self, player_id, max_players, width, height):
		# the player_id is an int, which can be converted to the name printed in the board
		self.player_name = "Erratic"
		# we will draw a random move every round
		self.moves = [D.up, D.left, D.down, D.right, D.up, D.up_left, D.down_left, D.down_right, D.up_right]
		#print("Hi there! We are playing ",self.status.params.rounds," rounds.")

	def round_begin(self, r):
		print("Welcome to round ",r,"---",self.status.params.rounds-r+1," to go.")
		pass

	def set_mines(self, status):
		"""
		set mines for fun
		"""

		map = status.map
		mines = []
		for i in range(5):
			if random.randint(0,100)<10:
				x,y = status.x,status.y
				x += random.randint(0,3)
				y += random.randint(0,3)

				if (x>=0 and x<map.width and y>=0 and y<map.height
				    and not map[x,y].is_blocked() and map[x,y].obj is None):
					mines.append((x,y))
			else: break
		return mines


	def move(self, status):
		# the status object (see game_utils.Status) contains:
		# - .player, our id, if we should have forgotten it
		# - .x and .y, our position
		# - .health and .gold, how much health and gold we have
		# - .map, a map of what we can see (see game_utils.Map)
		#   The origin of the map is in the lower left corner.
		# - .goldPots, a dict from positions to amounts
		# print("-" * 80)
		# print("Status for %s" % self.player_name)
		# # print the map as we can see it, along with health and gold
		# print(status)
		#print(status.map)  # the map can be printed too, but printing the status does this as well
		# for illustration, we go through the map and find stuff
		for x in range(status.map.width):
			for y in range(status.map.height):
				tile = status.map[x, y]
				# A tile has a 'status' and an object 'obj'.
				# See game_utils.TileStatus and game_utils.TileObject
				if tile.status == TileStatus.Wall:
					# we have discovered a wall!
					# which definitely shouldn't have any objects
					assert tile.obj is None
				obj = tile.obj
				if obj is not None:
					if obj.is_gold():
						# uhh, a pot of gold!
						amount = status.goldPots[x, y]
					else:
						assert obj.is_player()
						if obj.is_player(status.player):
							# we found our selfs
							assert (x, y) == (status.x, status.y)
						else:
							# we found someone else!
							other_player_id = obj.as_player()

		# make a random number of moves in a random direction
		numMoves = random.randint(0, 5)
		moves = []
		for i in range(numMoves):
			m = self.moves[random.randint(0, len(self.moves) - 1)]
			moves.append(m)
		return moves

class MyNonRandomPlayer(Player):
	def reset(self, player_id, max_players, width, height):
		self.player_name = "NonRandom" # nameFromPlayerId(player_id)
		self.ourMap = Map(width, height)

	def round_begin(self, r):
		pass

	def move(self, status):
		# print("-" * 80)
		# print("Status for %s" % self.player_name)
		# print(status)

		ourMap = self.ourMap
		# print("Our Map, before")
		# print(ourMap)
		for x in range(ourMap.width):
			for y in range(ourMap.height):
				if status.map[x, y].status != TileStatus.Unknown:
					ourMap[x, y].status = status.map[x, y].status
		# print("Our Map, after")
		# print(ourMap)


		neighbours = []
		for d in D:
			diff = d.as_xy()
			coord = status.x + diff[0], status.y + diff[1]
			if coord[0] < 0 or coord[0] >= status.map.width:
				continue
			if coord[1] < 0 or coord[1] >= status.map.height:
				continue
			tile = ourMap[coord]
			if tile.status != TileStatus.Wall:
				neighbours.append((d, coord))
		if len(neighbours) == 0:
			print("Seriously map makers? Thanks!")
			assert False

		assert len(status.goldPots) > 0
		gLoc = next(iter(status.goldPots))
		dists = []
		for d, coord in neighbours:
			dist = max(abs(gLoc[0] - coord[0]), abs(gLoc[1] - coord[1]))
			dists.append((d, dist))
		d, dist = min(dists, key=lambda p: p[1])

		#print("Gold is at", gLoc)
		#print("Best non-wall direction is", d, "with distance", dist)
		return [d]


players = [MyNonRandomPlayer(),
           MyRandomPlayer()]
