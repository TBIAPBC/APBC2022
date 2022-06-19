# A-Star Pathfinding
from game_utils import Direction as D
from game_utils import Tile, TileStatus, TileObject
import numpy as np


# Node
class Node():
    """ One tile in the map used for Pathfinding algortihms"""

    def __init__(self, parent=None, pos=None):
        self.parent = parent
        self.pos = pos  # (x,y) <-> (col,row)

        self.g = 0
        self.h = 0
        self.f = 0

    def initialize(self):
        self.g = self.h = self.f = 0

    def __sub__(self, other):
        x = self.pos[0] - other.pos[0]
        y = self.pos[1] - other.pos[1]
        return (x, y)

    def __str__(self):
        return "Node(x,y):" + str(self.pos)


class PQ():
    """Priority Queue"""

    def __init__(self):
        self.queue = []

    def __contains__(self, other):
        if not self.is_empty():
            for node in [j for i, j in self.queue]:
                if node.pos == other:
                    return True
        return False

    def is_empty(self):
        empty = True if len(self.queue) == 0 else False
        return empty

    def append(self, entry):
        self.queue.append(entry)

    def dequeue(self):
        if self.is_empty():
            return []
        else:
            self.queue.sort(key=lambda x: x[0], reverse=True)
            return self.queue.pop()

    def get_node(self, target_node):
        for idx, node in enumerate([j for i, j in self.queue]):
            if node == target_node:
                return node, idx
        return None, None

    def find(self, pos):
        if self.is_empty():
            return False
        for node in [j for i, j in self.queue]:
            if node.pos == pos:
                return True
            else:
                return False


def pathfinding_astar(maze, start, goal, status, directions=None):
    # cost = 1 (default)
    start_node = Node(None, start)
    start_node.initialize()  # set node values to zero
    goal_node = Node(None, goal)
    goal_node.initialize()
    visited = np.array(maze)

    # Initialize open and closed list
    # open_list = [start_node] # add start_node
    open_list = PQ()
    open_list.append((start_node.f, start_node))

    closed_list = []  # possibly dict

    # Loop till end of list

    while not open_list.is_empty():  # len(open_list) > 0:
        # Get current Node
        # current_node = open_list[0]
        # current_idx = 0
        current_node = open_list.dequeue()[1]  # lowest cost node
        closed_list.append(current_node)

        # Check if we found the goal
        if current_node.pos == goal_node.pos:
            path = []
            cur = current_node
            while cur is not None:
                path.append(cur.pos)
                cur = cur.parent
            return path[::-1]  # reverse path and return

        cur_pos = current_node.pos

        # Generate children
        if directions is None:
            directions = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1),
                          (-1, 1), (1, -1), (1, 1)]  # D.up ... D.down

        ### Experimental ###
        for new_pos in directions:
            # Node_pos = current_node + Node(None, new_pos)
            node_pos = (current_node.pos[0] + new_pos[0],
                        current_node.pos[1] + new_pos[1])

            x_ = node_pos[0]
            y_ = node_pos[1]

            visited[current_node.pos[0]][current_node.pos[1]] = 1  # visited

            # Make sure within range (is_Walkable)
            # if node_pos[0] > (len(map) - 1) or node_pos[0] < 0 or node_pos[1] > (len(map[len(map) - 1]) - 1) or node_pos[1] < 0:
            # continue  # TODO: check if correct, else think of mehcnaism

            if node_pos in closed_list:
                continue

            if 0 <= x_ < len(maze[0]) and 0 <= y_ < len(maze):
                state = status.map[x_, y_].status
                if state == TileStatus.Wall:
                    continue
                if visited[x_][y_] == 1:
                    continue
            else:
                continue

            visited[x_][y_] == 1  # we now visied it
            # Create a new node
            new_node = Node(current_node, node_pos)

            if not new_node in open_list:
                # idx = coor_dirs.index(new_node - current_node)
                idx = directions.index(new_node - current_node)
                # set_costs
                new_node.g = new_node.parent.g + 1  # self.dir_costs[dir_idx]
                # self.approx_distance(_node.coor)
                new_node.h = ((new_node.pos[0] - goal_node.pos[0])
                              ** 2) + ((new_node.pos[1] - goal_node.pos[1]) ** 2)
                new_node.f = new_node.g + new_node.h
                open_list.append((new_node.f, new_node))
            else:
                # if different_dir_costs:
                find_node, idx_f = open_list.get_node(new_node)
                if find_node.g < new_node.g:
                    open_list.queue[idx_f].parent = current_node
                    # dir_idx = coor_dirs.index(find_node - current_node)
                    dir_idx = directions.index(find_node - current_node)
                    # + self.dir_costs[dir_idx]
                    open_list.queue[idx_f].g = current_node.g
                    open_list.queue[idx_f].f = open_list.queue[idx_f].g + find_node.h

    # No path found!
    return []


# Create a Random Map
def rnd_map(width, height):
    _map = []
    for h in range(height):
        row = [w * 0 for w in range(width)]
        _map.append(row)
    return _map


# Create Direction dictionary
def dir_dict():
    dirs = {}
    dirs[(0, 1)] = D.up
    dirs[(0, -1)] = D.down
    dirs[(-1, 0)] = D.left
    dirs[(1, 0)] = D.right
    dirs[(-1, 1)] = D.up_left
    dirs[(1, 1)] = D.up_right
    dirs[(-1, -1)] = D.down_left
    dirs[(1, -1)] = D.down_right
    return dirs
