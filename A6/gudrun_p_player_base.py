
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
