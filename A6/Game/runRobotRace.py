#!/usr/bin/env python3
import random
import argparse
from importlib import import_module

from Game.game_utils import nameFromPlayerId
from Game.game_utils import Direction as D, MoveStatus
from Game.game_utils import Tile, TileStatus, TileObject
from Game.game_utils import Map, Status
from Game.simulator import Simulator
from Game.player_base import Player
from Game.register_robots import robot_module_names


def main(map_, density, viz, fps, number):

    robotmodules = {m: import_module(m) for m in robot_module_names.values()}

    if map_ is not None:
       m = Map.read(map_)
    else:
       m = Map.makeRandom(30, 30, density)

    sim = Simulator(map=m, vizfile=viz, framerate=fps)

    for name, module_name in robot_module_names.items():
        for p in robotmodules[module_name].players:
            p.player_modname = name
            sim.add_player(p)

    sim.play(rounds=number)
