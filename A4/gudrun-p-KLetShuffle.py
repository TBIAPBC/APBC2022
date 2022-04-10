# created by Gudrun Poetzelberger
# on 10. April 2022

import random as rd
import sys

N = 0
k = 0
args = sys.argv
assert len(args)==6, "Required program call format: gudrun-p-KLetShuffle.py -N 4 -k 2 KLetShuffle-test1.in"
assert args[1] == "-N" or args[3] == "-N", "Required program call format: gudrun-p-KLetShuffle.py -N 4 -k 2 KLetShuffle-test1.in"
assert args[1] == "-k" or args[3] == "-k", "Required program call format: gudrun-p-KLetShuffle.py -N 4 -k 2 KLetShuffle-test1.in"
if args[1] == "-N":
    N = int(args[2])
    k = int(args[4])
elif args[1] == "-k":
    k = int(args[2])
    N = int(args[4])
assert k >= 2, "k must be at least 2"
f = open(args[-1], "r")
sequence = f.read()
f.close()
if not sequence[-1].isalnum():  # remove the \n that is often at the end of the input files
    sequence = sequence[0:-1]

print("N = ", N)
print("k = ", k)