#!/usr/bin/env python3
import random

from game_utils import nameFromPlayerId
from game_utils import Direction as D, MoveStatus
from game_utils import Tile, TileStatus, TileObject
from game_utils import Map, Status
from simulator import Simulator
from player_base import Player

from shortestpaths import AllShortestPaths

class MyPathFindingPlayer(Player):

        def __init__(self,*,random=True):
                self.random=random

        def reset(self, player_id, max_players, width, height):
                self.player_name = "SillyScout"
                self.ourMap = Map(width, height)

        def round_begin(self, r):
                pass

        def _as_direction(self,curpos,nextpos):
                for d in D:
                        diff = d.as_xy()
                        if (curpos[0] + diff[0], curpos[1] + diff[1]) ==  nextpos:
                                return d
                return None

        def _as_directions(self,curpos,path):
                return [self._as_direction(x,y) for x,y in zip([curpos]+path,path)]

        def move(self, status):
                # print("-" * 80)
                # print("Status for %s" % self.player_name)
                # print(status)

                ourMap = self.ourMap
                #print("Our Map, before")
                #print(ourMap)
                for x in range(ourMap.width):
                        for y in range(ourMap.height):
                                if status.map[x, y].status != TileStatus.Unknown:
                                        ourMap[x, y].status = status.map[x, y].status
                #print("Our Map, after")
                #print(ourMap)

                curpos = (status.x,status.y)

                assert len(status.goldPots) > 0
                gLoc = next(iter(status.goldPots))

                goldInPot=list(status.goldPots.values())[0]

                ## determine next move d based on shortest path finding
                paths = AllShortestPaths(gLoc,ourMap)

                if self.random:
                        bestpath = paths.randomShortestPathFrom(curpos)
                else:
                        bestpath = paths.shortestPathFrom(curpos)

                bestpath = bestpath[1:]
                bestpath.append( gLoc )

                distance=len(bestpath)

                cost = status.params.cost
                #numMoves = random.randint(1, 5)
               
                #numMoves = max( numMoves 
                #                for numMoves in range(1,100)
                #               for totalCost in [(distance // numMoves)*cost(numMoves) 
                #                                  + cost(distance % numMoves)]
                #                if numMoves==1 or (totalCost < status.gold * 0.2
                #                                   and totalCost < goldInPot * 0.3)
                #)

                numMoves = 1

                ## don't move if the pot is too far away
                if numMoves>0 and distance/numMoves > status.goldPotRemainingRounds:
                        numMoves = 0
                        # print("SillyScout: I rather wait")

                return self._as_directions(curpos,bestpath[:numMoves])

players = [ MyPathFindingPlayer()]
