#!/usr/bin/env python3
from Game.game_utils import Direction as D
from Game.game_utils import TileStatus
from Game.game_utils import Map
from Game.player_base import Player
import numpy as np
import tempfile
from Game.shortestpaths import AllShortestPaths


class Anda(Player):

    def __init__(self, *, random=True):
        self.random = random

    def reset(self, player_id, max_players, width, height):
        self.player_name = "Anda"
        self.ourMap = Map(width, height)
        self.numMoves = 1
        self.memoryFile = tempfile.gettempdir() + '/Memory.npy'

        self.saveMemory()

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

    def update_map(self, status):  # Anda
        for x in range(self.ourMap.width):
            for y in range(self.ourMap.height):
                if self.ourMap[x, y].status == TileStatus.Unknown:
                    if status.map[x, y].status != TileStatus.Unknown:
                        self.ourMap[x, y].status = status.map[x, y].status

    def get_shortest_path_to_gold(self, curpos, status, map):  # Anda
        assert len(status.goldPots) > 0
        gLoc = next(iter(status.goldPots))
        # goldInPot=list(status.goldPots.values())[0]

        # shortest path
        paths = AllShortestPaths(gLoc, self.ourMap)

        if self.random:
            bestpath = paths.randomShortestPathFrom(curpos)
        else:
            bestpath = paths.shortestPathFrom(curpos)

        bestpath = bestpath[1:]
        bestpath.append(gLoc)  # add gold position
        return bestpath

    def visible_length(self, bestpath, status):
        moves = 0
        for i, j in enumerate(bestpath):
            moves = i + 1
            if self.ourMap[j].status == TileStatus.Unknown:

                break
        return moves

    def moving_cost(self, distance, numMoves):
        cost = sum([i + 1 for i in range(0, numMoves)])
        if numMoves == 0:
            return 100
        return (distance // numMoves) * cost

    def profit(self, status, cost, numMoves):
        return status.params.initialGoldPotAmount - cost - numMoves

    def how_far_to_go(self, bestpath, status):
        viz = self.visible_length(bestpath, status)
        while viz > 0 and ((status.gold - self.moving_cost(len(bestpath), viz)) < 10 or self.profit(status,
                                                                                                    self.moving_cost(
                                                                                                            len(bestpath),
                                                                                                            viz),
                                                                                                    viz) < 10):
            viz = viz - 1
            if viz == 0:
                return 0
        # the question is how much it pays off to move in each round
        return viz

    def should_move(self, bestpath, status):
        stay = False
        distance = len(bestpath)  # this is approximate when we still have areas not visible
        cost = status.params.cost
        viz = self.visible_length(bestpath, status)
        steps = self.how_far_to_go(bestpath, status)
        goldInPot = list(status.goldPots.values())[0]
        if steps == 0:
            return False

        ## when not to move:
        # 1. when gold disspears before I can reach it
        if len(bestpath) // steps > status.goldPotRemainingRounds:
            stay = True

        # if numMoves>0 and distance/numMoves > status.goldPotRemainingRounds:
        #         numMoves = 0
        #         print("Anda: I rather wait")
        #         stay=True


        # 2. If we do not make profit:
        # going for the gold costs more than the gold pot value ?? min profit ??
        # if goldInPot<=steps*self.moving_cost(distance,distance//steps):
        #         stay=True
        #         print("reason: NO GOOD PROFIT")
        # I wanna calculate if it pays off to try based on
        #        - distance to gold
        #        - how much it costs to move fast there
        #        - ho much of the path is known, take risk?

        # 1       #also stay if the remaining no of rounds does not allow reaching the gold
        # how many rounds left, wort it?
        #       stay=True

        # 2   # maybe explore map if still lots unknown and reachable!
        # when gold too far

        ##maybe even compare to gold of others?? not known!
        # 3

        ## don't move if the pot is too far away

        return not stay

    def profit(self, status, distance, numMoves):
        return status.params.initialGoldPotAmount - self.moving_cost(distance, numMoves)

    def move(self, status):
        self.refreshMemory(status)
        self.update_map(status)
        self.saveMemory()

        curpos = (status.x, status.y)

        bestpath = self.get_shortest_path_to_gold(curpos, status, self.ourMap)
        self.numMoves = self.how_far_to_go(bestpath, status)

        if self.should_move(bestpath, status):
            return self._as_directions(curpos, bestpath[:self.numMoves])
        else:
            return []

    def refreshMemory(self, status):
        with open(self.memoryFile, 'rb') as f:
            self.ourMap = np.load(f, allow_pickle=True)[0]

    def saveMemory(self):
        with open(self.memoryFile, 'wb') as f:
            np.save(f, [self.ourMap], allow_pickle=True)


players = [Anda()]