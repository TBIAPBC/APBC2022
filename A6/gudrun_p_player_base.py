import time  # sleep before print to avoid caching issues
from game_utils import Direction as D, MoveStatus

class Player(object):

	def reset(self, player_id, max_players, width, height):
		raise NotImplementedError("'reset' not implemented in '%s'." % self.__class__)

	def round_begin(self, r):
		raise NotImplementedError("'round_begin' not implemented in '%s'." % self.__class__)

	def move(self, status):
		raise NotImplementedError("'move' not implemented in '%s'." % self.__class__)

	def set_mines(self, status):
		"""
		Called to ask the player to set mines

		@param self the Player itself
		@param status the status
		@returns list of coordinates on the board

		The player answers with a list of positions, where mines
		should be set.

		Cost of setting mines:
		setting a mine in move distance k (as-the-eagle-flies, i.e.
		ignoring obstacles) to the player causes k actions.
		Actions are charged as usual.

		If a player does not define the method, this step is
		skipped.
		"""

		raise NotImplementedError("'setting mines' not implemented in '%s'." % self.__class__)



# --- Helper Functions (used by several robots) : ---
# written here so I don't have to copy-paste them into each robot class

	def _debugMessage(self, message):
		if self.printDebugMessages:
			time.sleep(0.00000001)
			print(self.player_name, ": ", message)

	def _as_direction(self, curpos, nextpos):
		# print("curpos = ", curpos)
		# print("nextpos = ", nextpos)
		for d in D:
			diff = d.as_xy()
			# print("for d = ", d, "aka diff = ", diff)
			# print("curpos[0] + diff[0], curpos[1] + diff[1] = " , curpos[0] + diff[0], curpos[1] + diff[1])
			if (curpos[0] + diff[0], curpos[1] + diff[1]) == nextpos:
				return d
		return None

	def _as_directions(self, curpos, path):
		# (zip: list of tuples, in this case tuples of tuples ((x1, y1),(x2, y2)), ((x2,y2),(x3,y3)), ... ?)
		return [self._as_direction(x, y) for x, y in zip([curpos] + path, path)]

	def _costOfMoves(self, numMoves):
		# Gauss summation of all numbers 0 to numMoves:
		cost = (numMoves + 1) * numMoves / 2.0
		return cost
