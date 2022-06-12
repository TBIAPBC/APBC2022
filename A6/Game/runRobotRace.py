#!/usr/bin/env python3
import random
from importlib import import_module

from Game.game_utils import Map, Status
from Game.simulator import Simulator
from Game.register_robots import robot_module_names


def main(map_, density, viz, fps, number, printing=False):

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

    sim.play(rounds=number, printing=printing)


def run_from_ui(map_, fps, rounds, robots):
    sim = Simulator(map=map_, framerate=fps)

    robots_for_game = {robot: robot_module_names[robot] for robot in robots}

    robot_modules = {m: import_module(m) for m in robots_for_game.values()}
    for name, module_name in robot_module_names.items():
        for p in robot_modules[module_name].players:
            p.player_modname = name
            sim.add_player(p)

    sim.play(rounds=rounds, printing=False)
