# first try: naive robots
# Robot 1: does not move at all, only collects gold for every round
# Robot 2: moves only 4 steps in the shortest path direction (to avoid spending too much on moving)

import random

from game_utils import nameFromPlayerId
from game_utils import Direction as D, MoveStatus
from game_utils import Tile, TileStatus, TileObject
from game_utils import Map, Status
from simulator import Simulator
from player_base import Player
from shortestpaths import AllShortestPaths


class MyRobot(Player):
    def __init__(self):
        self.player_name = "Tom"

    def reset(self, player_id, max_players, width, height):
        self.moves = [D.up, D.left, D.down, D.right, D.up, D.up_left, D.down_left, D.down_right, D.up_right]

    def round_begin(self, r):
        pass

    def move(self, status):
        curpos = (status.x, status.y)
        return self._as_directions(curpos, [])

    def _as_directions(self, curpos, path):
        return [self._as_direction(x, y) for x, y in zip([curpos] + path, path)]


class MyMovingRobot(Player):
    def __init__(self):
        self.player_name = "Jerry"

    def reset(self, player_id, max_players, width, height):
        self.myMap = Map(width, height)
        # print("map: ", self.myMap)

    def round_begin(self, r):
        pass

    def move(self, status):
        curpos = (status.x, status.y)

        myMap = self.myMap
        for x in range(myMap.width):
            for y in range(myMap.height):
                if status.map[x, y].status != TileStatus.Unknown:
                    myMap[x, y].status = status.map[x, y].status

        gLoc = next(iter(status.goldPots))

        self.gold_status = status.gold
        other_players = status.others

        player_coordinates = self.others_coords(other_players)

        ## determine next move d based on shortest path finding
        paths = AllShortestPaths(gLoc, self.myMap)

        shortestpath = paths.shortestPathFrom(curpos)
        shortestpath = shortestpath[1:]
        shortestpath.append(gLoc)

        if self.gold_status < 10:
            return self._as_directions(curpos, [], player_coordinates)
            shortestpath = []
        else:
            return self._as_directions(curpos, shortestpath[:4], player_coordinates)

    def others_coords(self, other_players):
        player_coords = []
        for element in other_players:
            if element:
                player_coords.append((element.x, element.y))

        return player_coords


    def moving_cost(self, path):  # probably static method?
        total_cost = 0
        if path:
            for i in range(1, len(path) + 1):
                total_cost += i

        return total_cost

    def _as_direction(self, curpos, nextpos, player_coordinates):
        neighbours = Map.nonWallNeighbours(self.myMap, curpos)
        neighbour_coords = []
        for element in neighbours:
            neighbour_coords.append(element[1])

        # print("neighbours: ", neighbour_coords)
        for d in D:
            diff = d.as_xy()
            if (curpos[0] + diff[0], curpos[1] + diff[1]) == nextpos:
                #print("next position: ", nextpos)
                if nextpos in neighbour_coords:
                    if nextpos in player_coordinates:
                        return "stop"
                    else:
                        return d
                else:
                    return "stop"
        return None

    def _as_directions(self, curpos, path, player_coordinates):

        directions = []
        for x, y in zip([curpos] + path, path):
            if self.gold_status == 0:
                break
            d = self._as_direction(x, y, player_coordinates)
            if d == "stop":
                break
            directions.append(d)
            # print(d)

        if directions == [None]:
            neighbours = Map.nonWallNeighbours(self.myMap, curpos)
            nextpos = random.choice(neighbours)
            d = self._as_direction(curpos, nextpos, player_coordinates)
            directions.append(d)

        # print("directions: ", directions)

        return directions
