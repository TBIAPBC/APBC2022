#!/usr/bin/env python3
from collections import deque
import copy
from game_utils import Direction as D, MoveStatus
from game_utils import Tile, TileStatus, TileObject
import random

import numpy as np

class AllShortestPaths:
    def __init__(self,sink,map):  # (?sink seems to be the position to which I want to calc the distances?)
        self.sink = sink
        self.map = map

        self.width=map.width
        self.height=map.height

        # self.wallmap = np.zeros((self.height, self.width), dtype='bool')

        # for x in range(self.width):
        #     for y in range(self.height):
        #         self.wallmap[x,y] = self.map[x,y].status == TileStatus.Wall
		
		# original:
        wm = [ [ self.map[x,y].status == TileStatus.Wall for y in range(self.height) ] for x in range(self.width) ]

		# see players and mines as walls:
        #wm = [ [ self.map[x,y].status.is_blocked() or (self.map[x,y].obj is not None and self.map[x,y].obj.is_player()) for y in range(self.height) ] for x in range(self.width) ]
		
        """
        wm = list()
        for x in range(self.width):
            wmrow = list()
            for y in range(self.height):
                if self.map[x,y].status.is_blocked():
                    wmrow.append(True)
                elif self.map[x,y].obj is not None:
                    print("There is an object at ", self.map[x,y])
                    if self.map[x,y].obj.is_player():
                        print("There is a player at ", self.map[x,y])
                        wmrow.append(True)
                else:
                    wmrow.append(False)
            wm.append(wmrow)
        """
		
        self.wallmap = np.array(wm,dtype='bool')
        #print("wallmap : ")
        #print(self.wallmap)
        self.dist = np.negative(np.ones((self.height, self.width), dtype='int'))

        self._calcDistances()

    # return the non-Wall neighbors of a field (x,y)
    def nonWallNeighborsIter(self,xy):

        (x,y) = xy
        xs=[x]
        if x>0: xs.append(x-1)
        if x<self.width-1: xs.append(x+1)

        ys=[y]
        if y>0: ys.append(y-1)
        if y<self.height-1: ys.append(y+1)

        for x in xs:
            for y in ys:
                if not self.wallmap[x,y]:
                    if (x,y)==xy: continue
                    yield (x,y)

    def _calcDistances(self):
        front = deque()  # (deque = doubly ended queue)
        front.append(self.sink)

        assert type(self.sink) == tuple
        self.dist[self.sink] = 0

        while front:
            xy=front.popleft()
            for neighbor in self.nonWallNeighborsIter(xy):
                if self.dist[neighbor]<0:
                    front.append(neighbor)
                    self.dist[neighbor] = self.dist[xy] + 1

    def shortestPathFrom(self, xy):
        if self.dist[xy]<0:
            return []

        path = list()
        curdist = self.dist[xy]

        while xy != self.sink:
            path.append(xy)

            # find preceeding neighbor
            for neighbor in self.nonWallNeighborsIter(xy):
                if self.dist[neighbor] ==  curdist-1:
                    curdist -= 1
                    xy = neighbor
                    break
        return path

    def randomShortestPathFrom(self, xy):
        if self.dist[xy]<0:
            return []

        path = list()
        curdist = self.dist[xy]

        while xy != self.sink:
            path.append(xy)

            potentialNextXYs = list()
            # find preceeding neighbor
            for neighbor in self.nonWallNeighborsIter(xy):
                if self.dist[neighbor] ==  curdist-1:
                    potentialNextXYs.append(neighbor)
            assert len(potentialNextXYs)>0
            xy = random.choice(potentialNextXYs)
            curdist -= 1
        return path
