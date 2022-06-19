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

        # Debug and Test
        # print("CurPos", curPos)
        goldInPot = list(status.goldPots.values())[0]

        # A-Star Pathfinding
        dirs = [d.as_xy() for d in self.moves]
        way = path(self.stage, curPos, gLoc, status, dirs)
        # Append path to moves for robot
        dist_est = self.estimate_dist(curPos, gLoc)
        threshold_d = int(min(width, height) * 0.75)
        # print("Track", dist_est, threshold_d)
        if dist_est <= threshold_d:
            moves = self.astar_way(curPos, way)
        else:
            moves = []

        return moves

    # Estimate distance btw two points

    def estimate_dist(self, curPos, goal):
        x, y = [abs(dx - dy) for dx, dy in zip(curPos, goal)]
        est = x + y - min(x, y)
        return est

    def astar_way(self, curPos, way, maxmoves=4):
        moves = []
        temp_pos = curPos
        nmoves = 0
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
