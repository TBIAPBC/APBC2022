

#!/usr/bin/env python3

from Game.game_utils import Direction as D
from Game.game_utils import TileStatus
from Game.game_utils import Map

from Game.player_base import Player
from Game.shortestpaths import AllShortestPaths



class Findklee(Player):



    def __init__(self, *, random=True):
        self.random = random
        self.give_up = False
        self.old_coord = (0, 0)
        self.player_name = "klee"

    def reset(self, player_id, max_players, width, height):
        self.ourMap = Map(width, height)
        #self.moves = [D.up, D.left, D.down, D.right, D.up, D.up_left, D.down_left, D.down_right, D.up_right]


    # print("Hi there! We are playing ",self.status.params.rounds," rounds.")

    def round_begin(self, r):
        pass

    def _as_direction(self, curpos, nextpos):
        for d in D:
            diff = d.as_xy()
            if (curpos[0] + diff[0], curpos[1] + diff[1]) == nextpos:
                return d
        return None

    def _as_directions(self, curpos, path):
        return [self._as_direction(x, y) for x, y in zip([curpos] + path, path)]



    def others_coordin(self, other_players):
        players_coordin = []
        for element in other_players:
            if element:
                players_coordin.append((element.x, element.y))

        return players_coordin

    def move(self, status):
        print("Status for %s" % self.player_name)

        ourMap = self.ourMap

        # print("Our Map, before")
        # print(ourMap)
        for x in range(ourMap.width):
            for y in range(ourMap.height):
                if status.map[x, y].status != TileStatus.Unknown:
                    ourMap[x, y].status = status.map[x, y].status
        # print("Our Map, after")
        # print(ourMap)

        curpos = (status.x, status.y)

        assert len(status.goldPots) > 0
        gLoc = next(iter(status.goldPots))

        goldInPot = list(status.goldPots.values())[0]

        # status.goldPotRemainingRounds

        ## determine next move d based on shortest path finding
        paths = AllShortestPaths(gLoc, ourMap)

        # if self.random:
        #        bestpath = paths.randomShortestPathFrom(curpos)
        # else:
        bestpath = paths.shortestPathFrom(curpos)

        bestpath = bestpath[1:]
        bestpath.append(gLoc)
        unknown = False
        player_blocking = False

        other_players = status.others
        player_coordinates = self.others_coordin(other_players)

        # from DenSki
        for step in bestpath:
            if ourMap[step].status == TileStatus.Unknown:
                unknown = True
            if step in player_coordinates:
                player_blocking = True
                self.give_up = True
                for coord, amount in status.goldPots.items():
                    self.old_coord = coord
        if self.give_up:
            for coord, amount in status.goldPots.items():
                if coord != self.old_coord:
                    self.give_up = False

        distance = len(bestpath)


        cost = 0
        for i in range(0, distance):
            i = i + 1
            cost += i


        numMoves = 2
        rounds_needed = distance / 2

        if rounds_needed <= 6 and not player_blocking and not unknown and not self.give_up and goldInPot > cost:
            numMoves = distance
        print(f"statusgold {status.goldPotRemainingRounds}")

        if distance/numMoves > int(status.goldPotRemainingRounds/2) and not player_blocking and not self.give_up:
            numMoves = 1
        # if rounds_needed > 4 and not player_blocking and goldInPot > cost:
        #     numMoves = 2



        elif distance/numMoves > status.goldPotRemainingRounds or cost >= goldInPot:
            numMoves = 0
        print("I rather wait")
        print(f"status.gold: {status.gold}")
        print(f"goldInPot: {goldInPot} versus cost: {cost}")



        return self._as_directions(curpos, bestpath[:numMoves])


players = [Findklee()]