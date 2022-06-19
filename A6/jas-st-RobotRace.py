#!/usr/bin/env python3
import random

from game_utils import nameFromPlayerId
from game_utils import Direction as D, MoveStatus
from game_utils import Tile, TileStatus, TileObject
from game_utils import Map, Status
from simulator import Simulator
from player_base import Player

from shortestpaths import AllShortestPaths

### performs well against slow robots, but not very successfull against faster ones
class Minesweeper(Player):

        def reset(self, player_id, max_players, width, height):
                self.player_name = "Minesweeper"
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

        #update known map each step
        def update_map(self, status):
                for x in range(self.ourMap.width):
                        for y in range(self.ourMap.height):
                                if status.map[x, y].status != TileStatus.Unknown:
                                        self.ourMap[x, y].status = status.map[x, y].status
        
        #finds shortest path to the gold pot
        def find_path(self, start_pos, destination):
                path = AllShortestPaths(destination, self.ourMap).shortestPathFrom(start_pos)
                path.append(destination)
                return path[1:]

        # checks if there is going to be a crash along the path
        def crash_check(self, path, status):
                others_stat = status.others
                others_pos = []
                others_pos_extended = []
                for i in range(len(others_stat)):
                        if others_stat[i] is not None:
                                others_pos.append((others_stat[i].x, others_stat[i].y))

        #to try and prevent crashes with other robots it checks whether there is a robot along the path,
        #or if a robot is near the path (within 1 square distance)
                mov = [-1,0,1]
                if len(others_pos) != 0:
                        for position in others_pos:
                                for i in mov:
                                        for j in mov:
                                                others_pos_extended.append((position[0]+i, position[i]+j))
                                                

                crash = False
                for i in range(len(path)):
                        #print(path[i])
                        #print(others_pos)
                        #print(self.ourMap[path[i]].status)
                        if self.ourMap[path[i]].status != TileStatus.Empty or any(path[i] == x_pos for x_pos in others_pos_extended):
                                crash = True
                                crash_pos = i
                                break
                
                if crash:
                        return path[:crash_pos]
                else:
                        return path


        def move(self, status):
                self.update_map(status)
                current_position = (status.x, status.y)

                goldPot = next(iter(status.goldPots))
                path = self.find_path(current_position, goldPot)
                cost_for_path = status.params.cost(len(path))

                path = self.crash_check(path, status)


         ### this is still under construction, basically it should move very fast when the gold pot is within range
         ### and take steps of 4 if it can afford it
                if cost_for_path >= 0.3*status.gold and status.gold > 50:
                        return self._as_directions(current_position, path[:4])
                elif status.gold <= 50:
                        return self._as_directions(current_position, [])
                elif status.gold - cost_for_path + status.goldPots[goldPot] > status.gold :
                        return self._as_directions(current_position, path)
                elif status.gold - cost_for_path <= 100 : 
                        return self._as_directions(current_position, [])
                else:
                        return self._as_directions(current_position, path[:4])


players = [ Minesweeper()]

