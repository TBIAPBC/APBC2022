from game_utils import Map, TileStatus, Direction
from player_base import Player
from shortestpaths import AllShortestPaths

"""
Follower (not implemented yet): Choose player with highest amount of gold, follow this player and set mines between the player and the gold pot.
"""


"""
Casual: Just moves along the shortest path and tries to get the gold first. 
"""


class Casual(Player):
    def reset(self, player_id, max_players, width, height):
        self.player_name = "Casual"
        self.map = Map(width, height)
        self.min_gold = 0.2

    def round_begin(self, r):
        pass

    def move(self, status):
        # update stored map with given map
        self.update_map(status.map)
        # get some parameter
        game_parameter = status.params
        cost = game_parameter.cost
        other_players = status.others
        # get current position
        current_position = (status.x, status.y)
        # get the position of the gold pot
        gold_pot_position = next(iter(status.goldPots))
        # get all shortest paths to the gold pot
        paths = AllShortestPaths(gold_pot_position, self.map)
        # get the shortest path from my current position to the gold pot
        best_path = paths.shortestPathFrom(current_position)
        best_path.append(gold_pot_position)
        # check how many steps can be done with remaining gold no matter how much
        # money is in the pot; don't move if it is to far away
        distance = len(best_path[1:])
        if cost(distance) // 2 > status.gold or distance >= 20:
            return []

        save_moves = self.check_map(best_path, status.x, status.y)

        # calculate possible moves with current gold
        number_moves = max([x for x in range(1, 100) if cost(x) < (status.gold // self.min_gold)])

        if save_moves < number_moves:
            number_moves = save_moves

        return self.get_directions(current_position, best_path[1:number_moves])

    # check map if there are walls, players or mines
    def check_map(self, best_path, x, y):
        save_moves = 0
        for i, coordinates in enumerate(best_path[1:]):
            tile = self.map[coordinates[0], coordinates[1]]
            current_object = tile.obj
            if current_object is not None:
                if current_object.is_player() and (coordinates[0], coordinates[1]) != (x, y):
                    save_moves = i
                    break
                if current_object.is_gold():
                    continue
            if tile.status != TileStatus.Empty:
                save_moves = i
                break
            save_moves = i
        save_moves += 2
        return save_moves

    def get_directions(self, current_position, path):
        steps = []
        for current_position, next_position in zip([current_position] + path, path):
            for direction in Direction:
                direction_coordinates = direction.as_xy()
                if (current_position[0] + direction_coordinates[0],
                    current_position[1] + direction_coordinates[1]) == next_position:
                    steps.append(direction)
        return steps

    def update_map(self, map):
        if self.map is None:
            self.map = map
            return

        for x in range(self.map.width):
            for y in range(self.map.height):
                if map[x, y].status != TileStatus.Unknown:
                    if self.map[x, y].status == TileStatus.Unknown:
                        self.map[x, y].status = map[x, y].status

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


players = [Casual()]
