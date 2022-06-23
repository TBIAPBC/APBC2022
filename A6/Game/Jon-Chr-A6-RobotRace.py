from Game.game_utils import Direction as D
from Game.game_utils import Map
from Game.player_base import Player

from Game.jonchr_utilities import pathfinding_astar as path, rnd_map as rm
from Game.jonchr_utilities import dir_dict as dd


class MyRobot(Player):

    def __init__(self):
        self.player_name = "JonChr"
        self.init_gold = 0
        self.max_gold = 0
        self.isFirst = True

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
        pass

    def move(self, status):
        ourMap = self.current_map
        others = status.others

        width = ourMap.width
        height = ourMap.height

        # Initialize
        if self.isFirst:
            self.isFirst = False
            self.init_gold = status.gold
            self.max_gold = self.init_gold

        # Robot Scaling
        self.max_gold = status.gold if status.gold > self.max_gold else self.max_gold
        # Check how much gold increased or decreased
        maxmoves, thres = self.robot_scaling(status)

        # Current Position
        curPos = (status.x, status.y)

        # Gold Position
        assert len(status.goldPots) > 0
        gLoc = next(iter(status.goldPots))  # gLoc = (x,y)
        goldInPot = list(status.goldPots.values())[0]

        # A-Star Pathfinding. Append Path
        dist_est = self.estimate_dist(curPos, gLoc)
        threshold_d = int(min(width, height) * thres)

        # If gold not to far away
        if dist_est <= threshold_d:
            dirs = [d.as_xy() for d in self.moves]
            way = path(self.stage, curPos, gLoc, status, dirs)
            moves = self.astar_way(curPos, way, maxmoves)
        else:
            # Wait
            moves = []

        return moves

    # Estimate distance btw two points

    def estimate_dist(self, curPos, goal):
        x, y = [abs(dx - dy) for dx, dy in zip(curPos, goal)]
        est = x + y - min(x, y)
        return est

    # Convert Pathway to Move-Set
    def astar_way(self, curPos, way, maxmoves=4):
        moves = []
        temp_pos = curPos
        nmoves = 0
        for direc in way:
            nmoves += 1
            # Upper-limit
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

    # Scale Robot Moves and Gold-detect radius based on gold
    def robot_scaling(self, status):
        # Check how much gold increased or decreased
        # scale-times init gold
        scale_i = int(self.max_gold / self.init_gold)
        # scales-amount of max gold
        scale_cur = int(status.gold / self.max_gold)
        factor_m = int(scale_i * scale_cur)
        factor_t = round((factor_m / 100), 2)
        temp = 0.75 + factor_t
        # End values
        maxmove = factor_m if factor_m > 4 else 4
        maxmoves = maxmove if maxmove < 10 else 10
        thres = temp if temp < 0.85 else 0.75
        return maxmoves, thres


players = [MyRobot()]