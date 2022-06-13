"""
Interface Models to Game
"""
from matplotlib import pyplot as plt


class RoundData:
    def __init__(self, round_, map_, colors):
        self.colors = colors
        self.round = round_
        self.player = []
        self.health = {}
        self.gold = {}

        # image relevant
        self.pos = {}
        self.gold_pos = []
        self.gold_amount = 0
        self.map_ = map_
        self.round = round_
        self.map = map_
        self.width = map_.width
        self.height = map_.height
        self.markersize = (200*900)/(self.width*self.height)
        self.linewidth = (7*900)/(self.width*self.height)

        self.__img_find_walls()

    def __str__(self):
        s = str(self.round) + str(self.player) + str(self.gold) + str(self.health) + "\n\n\n" + str(self.map_) + "\n\n\n"
        return s

    def add_player(self, player, health, gold, pos):
        if player not in self.player:
            self.player.append(player)
        self.health[player] = health
        self.gold[player] = gold
        self.pos[player] = pos

    def set_gold_pos(self, pos, amount):
        self.gold_pos = pos
        self.gold_amount = amount

    def __img_find_walls(self):
        self.walls = [(x, y) for y, row in enumerate(self.map._data) for x, tile in enumerate(row) if str(tile) == '#']

    def __img_plot(self):
        self.ax.tick_params(
            bottom=False,
            left=False,
        )
        self.ax.set_yticklabels([])
        self.ax.set_xticklabels([])

        self.ax.set_ylim(top=self.height-0.5, bottom=-0.5)
        self.ax.set_xlim(left=-0.5, right=self.width-0.5)

    def __img_walls(self):
        x, y = list(zip(*self.walls))
        self.ax.scatter(x=x, y=y, marker='s', c='grey', s=self.markersize, edgecolors='w')

    def __img_robots(self):
        x, y = [], []
        for robot in self.player:
            pos = self.pos[robot]
            x.append(pos[0])
            y.append(pos[1])

        self.robot = self.ax.scatter(
            x=x, y=y, edgecolors='k',
            c=self.colors, vmin=0, vmax=100, cmap='Reds_r', zorder=2, marker='D')

        self.robot.set_sizes([self.gold[i] for i in self.player])

    def __img_goldpots(self):
        self.goldpots = self.ax.scatter(
            x=self.gold_pos[0], y=self.gold_pos[1], marker='*', edgecolors='k', c='gold')
        self.goldpots.set_sizes([self.gold_amount])

    def save_image(self):
        # init image
        title = f"./Tmp//sim_{self.round}.png"
        fig, self.ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 8))

        # modify image style

        # fill plot
        #self.__img_find_walls()
        self.__img_plot()
        self.__img_walls()
        self.__img_robots()
        self.__img_goldpots()

        # save img
        fig.savefig(title, bbox_inches="tight", pad_inches=0.02)


class Settings:
    def __init__(self):
        # map
        self.random_map = True
        self.random_width = 30
        self.random_height = 30
        self.random_density = 0.4
        self.preset_map = None

        # robots
        self.robots = []

        # rounds
        self.rounds = 1000

    def __str__(self):
        if self.random_map is True:
            s = f"width: {self.random_width}, y: {self.random_height}, d: {self.random_density}, " \
                f"robots: {self.robots}, rounds: {self.rounds}"
        else:
            s = f"preset: {self.preset_map}, robots: {self.robots}, rounds: {self.rounds}"
        return s
