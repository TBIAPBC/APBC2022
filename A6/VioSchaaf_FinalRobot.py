import random

from game_utils import nameFromPlayerId
from game_utils import Direction as D, MoveStatus
from game_utils import Tile, TileStatus, TileObject
from game_utils import Map, Status
from simulator import Simulator
from player_base import Player
from shortestpaths import AllShortestPaths


class VioSchaafRobot(Player):
    def __init__(self):
        self.player_name = "VioSchaaf"

    def reset(self, player_id, max_players, width, height):
        self.myMap = Map(width, height)
        # print("map: ", self.myMap)

    def round_begin(self, r):
        pass

    def move(self, status):

        # current postition
        curpos = (status.x, status.y)

        # save status of all visible tiles
        myMap = self.myMap
        for x in range(myMap.width):
            for y in range(myMap.height):
                if status.map[x, y].status != TileStatus.Unknown:
                    myMap[x, y].status = status.map[x, y].status

        # gold pot location and gold amount
        gLoc = next(iter(status.goldPots))
        goldpot_amount = self.gold_amount(status, gLoc)

        # my own gold amount
        self.gold_status = status.gold

        # coordinates of other players
        other_players = status.others
        player_coordinates = self.others_coords(other_players)

        # add other players to map (pretend they are walls to avoid collisions)
        map_with_players = myMap
        for p in player_coordinates:
            map_with_players[p].status = TileStatus.Wall

        # determine next move d based on shortest path finding
        paths = AllShortestPaths(gLoc, map_with_players)

        shortestpath = paths.shortestPathFrom(curpos)
        shortestpath = shortestpath[1:]
        shortestpath.append(gLoc)

        # check if status of all tiles in path is known
        path_known = self.check_status(status, shortestpath)

        # avoid crashes by checking if two robots are at the same position after a the same number of moves
        # (assuming they use the shortestpath function)
        avoid_crash = self.check_crash(player_coordinates, shortestpath, paths)

        # if tile status is known for the entire path and there is as much gold as needed to get there + some extra
        # and if no other player is closer to the gold: go to get the gold immediately
        # else: move only four steps towards the gold (if there is enough gold and the pot can be reached in time)
        # if the pot cannot be reached within the remaining rounds with the amount of gold:
        # stop moving and wait until the pot changes its position

        rounds_needed = len(shortestpath)/4

        if path_known and self.others_path(player_coordinates, len(shortestpath), paths) and avoid_crash:

            if self.moving_cost(shortestpath) < goldpot_amount + 25:
                return self._as_directions(curpos, shortestpath, player_coordinates)
            else:

                if self.gold_remaining_rounds(status) >= rounds_needed and (self.gold_status >= (10 * rounds_needed)):
                    return self._as_directions(curpos, shortestpath[:4], player_coordinates)
                else:
                    return self._as_directions(curpos, [], player_coordinates)


        elif self.gold_status >= (10 * rounds_needed) and (self.gold_remaining_rounds(status) >= rounds_needed):
            return self._as_directions(curpos, shortestpath[:4], player_coordinates)

        else:
            return self._as_directions(curpos, [], player_coordinates)

    def gold_remaining_rounds(self, status):
        # returns number of rounds until gold pot is emptied
        gold_rounds = status.goldPotRemainingRounds
        return gold_rounds

    def check_status(self, status, path):
        # checks if status of every tile of shortest path is known
        for x, y in path:
            if status.map[x, y].status == TileStatus.Unknown:
                path_known = False
                return path_known
            else:
                path_known = True
        return path_known

    def others_path(self, coords_others, pathlength, paths):
        # checks if paths of other players with known positions is shorter
        shortest = True
        for coords in coords_others:
            if len(paths.shortestPathFrom(coords)) < pathlength:
                shortest = False

        return shortest

    def check_crash(self, coords_others, shortestpath, paths):
        # checks if robot might crash into other players (assuming they use the shortestpath function)
        no_crash = True

        for coords in coords_others:
            other_path = paths.shortestPathFrom(coords)[1:]
            min_length = min(len(other_path), len(shortestpath))

            for i in range(min_length):
                if other_path[i] == shortestpath[i]:
                    no_crash = False
                    break

        return no_crash

    def gold_amount(self, status, gloc):
        # returns gold amoung
        gold = status.goldPots[gloc]
        print("gold: ", gold)
        return gold

    def others_coords(self, other_players):
        # returns coordinates of other visible players
        player_coords = []
        for element in other_players:
            if element:
                player_coords.append((element.x, element.y))

        return player_coords


    def moving_cost(self, path):
        # returns moving cost of a given path
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

        for d in D:
            diff = d.as_xy()
            if (curpos[0] + diff[0], curpos[1] + diff[1]) == nextpos:
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

        return directions



