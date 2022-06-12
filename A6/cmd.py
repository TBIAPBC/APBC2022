import argparse
from Game import runRobotRace


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Robot Race Simulator 7000")
    parser.add_argument('--viz', help="filename for the visualization of the race", type=str)
    parser.add_argument('--number', help="number of rounds", type=int, default=10)
    parser.add_argument('--density', help="map density", type=float, default=0.4)
    parser.add_argument('--framerate', help="specify framerate of the visualization", type=int, default=8)
    parser.add_argument('--map', help="specify map file", type=str)
    parser.add_argument("-p", "--print", store_action=True)
    args = parser.parse_args()

    if args.print():
        runRobotRace.main(map_=args.map, density=args.density, viz=args.viz, fps=args.framerate, number=args.number, printing=True)
    else:
        runRobotRace.main(map_=args.map, density=args.density, viz=args.viz, fps=args.framerate, number=args.number, printing=False)
