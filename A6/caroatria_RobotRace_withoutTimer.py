#!/usr/bin/env python3
import random
from game_utils import nameFromPlayerId
from game_utils import Direction as D, MoveStatus
from game_utils import Tile, TileStatus, TileObject
from game_utils import Map, Status
from simulator import Simulator
from player_base import Player#
#from caroatria_player_base import Player

from shortestpaths import AllShortestPaths #possibly modify

class MyPathFindingPlayer(Player):
        starting_point = (0,0)

        def __init__(self,*,random=True):
                self.random=random

        def reset(self, player_id, max_players, width, height):
                self.player_name = "CasualCaro"
                self.ourMap = Map(width, height)

        def round_begin(self, r):
                pass #null statement, placeholder for future code

        def _as_direction(self,curpos,nextpos): #curpos = current position
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
                # print("map type is", type(ourMap))
                for x in range(ourMap.width):
                        for y in range(ourMap.height):
                                if status.map[x, y].status != TileStatus.Unknown:
                                        ourMap[x, y].status = status.map[x, y].status
                #print("Our Map, after")
                #print(ourMap)
                curpos = (status.x,status.y) #current pos?
                # midx = ourMap.width/2
                # midy = ourMap.height/2
                middle_point =(15,15)
                # middle_point = (midx,midy)
                midx = middle_point[0]
                midy = middle_point[1]
                if ourMap[midx, midy].status == TileStatus.Empty:
                        middle_point = (midx,midy)
                else:
                        counter = 0
                        while ourMap[midx, midy].status != TileStatus.Empty:
                                if counter < 50:
                                        midx = int((midx + curpos[0])/2)
                                        midy = int((midy + curpos[1])/2)
                                        counter += 1
                                else:
                                        middle_point = (15,15)
                                        counter = 0

                middle_point = (midx,midy)
                
                # print("chosen middle point",middle_point)
                
                # print("middle point",middle_point)
                

                assert len(status.goldPots) > 0 #if false, assertion error raised
                gLoc = next(iter(status.goldPots)) #x,y coord of first gold pot

                goldInPot=list(status.goldPots.values())[0] #value of pot,

                ## determine next move d based on shortest path finding
                paths = AllShortestPaths(gLoc,ourMap)
                path_to_middle = AllShortestPaths(middle_point,ourMap)

                if self.random:
                        bestpath = paths.randomShortestPathFrom(curpos)
                        best_middle_path = path_to_middle.randomShortestPathFrom(curpos)
                else:
                        bestpath = paths.shortestPathFrom(curpos)
                        best_middle_path = path_to_middle.shortestPathFrom(curpos)


                bestpath = bestpath[1:] #where we calculate path from fold to player
                bestpath.append( gLoc )

                distance=len(bestpath)

                cost = status.params.cost

                numMoves = 1

                ## don't move if the pot is too far away
                ##instead move closer to the center
                if numMoves>0 and distance/numMoves > status.goldPotRemainingRounds:
                        # bestpath = best_middle_path[1:]
                        bestpath.append(best_middle_path[1:])
                elif goldInPot > 50 and distance < 10: #sprint if its worth it
                        numMoves += 1
                print("will mov", self._as_directions(curpos,bestpath[:numMoves]))
                return self._as_directions(curpos,bestpath[:numMoves])

players = [ MyPathFindingPlayer()]