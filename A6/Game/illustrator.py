import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np


class Illustrator:
    def __init__(self, m, vizfile, framerate):
        self.robotspos = []
        self.robotshealth = []
        self.robotsmoney = []
        self.goldpos = []
        self.goldamount = []
        self.minepos = []
        self.minetime = []

        self.width = m.width
        self.height = m.height
        self.markersize = (200*900)/(self.width*self.height)
        self.linewidth = (7*900)/(self.width*self.height)

        self.find_walls(m)

        self.FRAME_PER_SECOND = framerate
        self.vizfile = vizfile

    def find_walls(self, m):
        self.walls = [
            (x, y)
            for y, row in enumerate(m._data)
            for x, tile in enumerate(row)
            if str(tile) == '#'
        ]

    def _add_robots(self, robots):
        self.n_robots = len(robots)
        self.robot_names = [robot.player_name for robot in robots]

    def _add_nrounds(self, rounds):
        self.n_rounds = rounds

    def append_robots(self, robots):
        rpos, rhealth, rmoney = [], [], []
        for robot in robots:
            rpos.append([robot.status.x, robot.status.y])
            rhealth.append(robot.status.health)
            rmoney.append(robot.status.gold)

        maxmoney = max(rmoney)
        rmoney = [80*money/maxmoney+25 for money in rmoney]

        self.robotspos.append(rpos)
        self.robotshealth.append(rhealth)
        self.robotsmoney.append(rmoney)

    def append_goldpots(self, goldpots):
        self.goldpos.append(list(goldpots.keys()))
        self.goldamount.append(list(goldpots.values()))

    def append_mines(self, mines):
        minepos = list(mines.keys()) + [(-1,-1)]
        minepos = minepos*5
        minepos = minepos[:5]
        self.minepos.append(minepos)
        self.minetime.append(list(mines.values()))

    def _illustrate(self):
        fig, self.ax = plt.subplots(
            nrows=1, ncols=1, figsize=(8, 8))

        self.init_plot()
        self.init_walls()
        self.init_robots()
        self.init_trails()
        self.init_goldpots()
        self.init_mines()

        gif = FuncAnimation(fig, self.illustrate_round,
                            self.n_rounds)

        gif.save(self.vizfile,
                 dpi=80, fps=self.FRAME_PER_SECOND)

    def init_plot(self):
        self.ax.tick_params(
            bottom=False,
            left=False,
        )
        self.ax.set_yticklabels([])
        self.ax.set_xticklabels([])

        self.ax.set_ylim(top=self.height-0.5, bottom=-0.5)
        self.ax.set_xlim(left=-0.5, right=self.width-0.5)

    def init_walls(self):
        x, y = list(zip(*self.walls))
        self.ax.scatter(x=x, y=y, marker='s', c='grey', s=self.markersize, edgecolors='w')

    def init_trails(self):
        self.trails = [
            self.ax.plot([], [], alpha=0.5, linewidth=self.linewidth,zorder=1, label=self.robot_names[i])[0]
            for i in range(self.n_robots)
        ]
        self.ax.legend(loc='upper right', bbox_to_anchor=(
            0.05, 1.15), prop=dict(size=8))

    def init_robots(self):
        self.robot = self.ax.scatter(
            x=[], y=[], edgecolors='k', vmin=0, vmax=100, c=[], cmap='Reds_r', zorder=2, marker='D')

    def init_goldpots(self):
        self.goldpots = self.ax.scatter(
            x=[], y=[], marker='*', edgecolors='k', c='gold')

    def init_mines(self):
        self.mines = self.ax.scatter(
            x=[], y=[], marker='X', edgecolors='k', c='red')

    def illustrate_round(self, i):
        def pivot(array):
            return list(zip(*array))

        if not (i+1) % 10:
            print('illustrating step', i+1)

        # figure
        title = str(i+1)
        self.ax.set_title(title, fontsize=20)

        # goldpots
        self.goldpots.set_offsets(self.goldpos[i])
        self.goldpots.set_sizes(self.goldamount[i])

        # robots
        self.robot.set_offsets(self.robotspos[i])
        self.robot.set_sizes(self.robotsmoney[i])
        self.robot.set_array(np.array(self.robotshealth[i]))

        # mines
        self.mines.set_offsets(self.minepos[i])

        # trails
        lo = [0, i-5][i-5 >= 0]
        offsets = pivot(self.robotspos[lo:i+1])
        for trail, offset in zip(self.trails, offsets):
            x, y = pivot(list(offset))
            trail.set_data(list(x), list(y))
