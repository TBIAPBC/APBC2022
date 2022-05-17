#!/usr/bin/env python3
import random
import argparse

from game_utils import nameFromPlayerId
from game_utils import Direction as D, MoveStatus
from game_utils import Tile, TileStatus, TileObject
from game_utils import Map, Status
from simulator import Simulator
from player_base import Player

parser = argparse.ArgumentParser(description="Robot Race Simulator 7000")
parser.add_argument('--viz', help="filename for the visualization of the race", type=str)
parser.add_argument('--number', help="number of rounds", type=int, default=1000)
parser.add_argument('--density', help="map density", type=float, default=0.4)
parser.add_argument('--framerate', help="specify framerate of the visualization", type=int, default=8)
parser.add_argument('--map', help="specify map file", type=str,default=None)

args = parser.parse_args()

robot_module_names = {"Test":"test-RobotRace",
		      "Beatme": "beatme-RobotRace",
			  "GudrunsBots": "gudrun-p-RobotRace"}

robotmodules = { m:__import__(m) for m in robot_module_names.values() }

if args.map is not None:
   m = Map.read(args.map)
else:
   m = Map.makeRandom(30, 30, args.density)

sim = Simulator(map=m, vizfile=args.viz, framerate=args.framerate)

for name,module_name in robot_module_names.items():
	for p in robotmodules[module_name].players:
		p.player_modname = name
		sim.add_player(p)

sim.play(rounds=args.number)
