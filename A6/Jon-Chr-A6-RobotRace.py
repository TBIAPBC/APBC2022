import sys
import random

from game_utils import nameFromPlayerId
from game_utils import Direction as D, MoveStatus
from game_utils import Tile, TileStatus, TileObject
from game_utils import Map, Status
from simulator import Simulator
from player_base import Player

from jonchr_utilities import Node, pathfinding_astar as path, PQ, rnd_map as rm
from jonchr_utilities import dir_dict as dd

import numpy as np


class MyRobot(Player):

    def __init__(self):
        self.player_name = "JonChr"
        self.waymem = []
        self.goldmem = None
        self.playermem = None
        self.curIt = -1
        self.init = False

    def reset(self, player_id, max_players, width, height):
        # Reset every Round
        self.player_name = "JonChr"
        self.map_width = width
        self.map_height = height
        self.current_map = Map(width, height)
        self.max_players = max_players
        self.moves = [D.up, D.left, D.down, D.right, D.up,
                      D.up_left, D.down_left, D.down_right, D.up_right]
        self.ddict = dd()
        self.stage = rm(width, height)

    def round_begin(self, r):
        print("Where is the gold?")

    def move(self, status):
        moves = []
        ourMap = self.current_map
        others = status.others

        width = ourMap.width
        height = ourMap.height

        for x in range(width):
            for y in range(height):
                if status.map[x, y].status != TileStatus.Unknown:
                    ourMap[x, y].status = status.map[x, y].status

        # Current Position
        curPos = (status.x, status.y)

        # Gold Position
        assert len(status.goldPots) > 0
        gLoc = next(iter(status.goldPots))  # gLoc = (x,y)

        wm = [[ourMap[x, y].status == TileStatus.Wall for y in range(height)]
              for x in range(width)]

        wallmap = np.array(wm, dtype="bool")
        # print(wallmap)

        # Debug and Test
        print("CurPos", curPos)
        print("GLoc", gLoc)
        print("Health", status.health)
        print("Gold", status.gold)

        goldInPot = list(status.goldPots.values())[0]

        # TODO: Map
        # level = saveMap(wm, self.stage)
        # Radius around Char
        # level = list([map(int, x) for x in wm])
        # print("TEST", wallmap[7][1], wallmap[7][1] == True)

        if self.init == False:
            dirs = [d.as_xy() for d in self.moves]
            way = path(wallmap, curPos, gLoc, status, dirs)
        # print("Way:", way)

            """
        # Memory of Gold Pos
        if self.init == False:
            self.goldmem = gLoc
            self.playermem = curPos
            self.waymem = way
            self.curIt = 0
            self.init = True

        # Player has not moved
        if self.playermem == curPos and self.init == True:
            # Make a random move
            way = []
            self.init = False
            pass

        # Check Memory fo Gold Pos if changed
        if self.goldmem != gLoc:
            self.init = False
            pass

        self.goldmem = gLoc
        self.playermem = curPos
        self.curIt += 1
        """

        if len(way) == 0:
            print("Empty")

        # Append path to moves for robot
        temp_pos = curPos
        nmoves = 0
        maxmoves = 4  # 3 moves
        for direc in way:
            nmoves += 1
            if nmoves > maxmoves:
                break
            # compute coord
            dx = direc[0] - temp_pos[0]
            dy = direc[1] - temp_pos[1]
            dpos = (dx, dy)
            temp_pos = direc
            if dx == 0 and dy == 0:
                continue
            else:
                myMove = self.ddict[dpos]
                moves.append(myMove)

        return moves


players = [MyRobot()]
