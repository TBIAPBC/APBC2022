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

sequence = "CUUUUGCUAG"  # for testing
k = 3  # for testing
#"""
adjacencyDictionary = {}  # I want to create a 2D dictionary "matrix", aka a dictionary of dictionaries,
## so that I can call things like adjacentDictionary['UU']['UC'], and the result is the number of edges 'UU'->'UC'
## I am using a dictionary and not an array or list because I need to be able to call it by key (subsequence-string, e.g. 'UC')
i = 0
while i < len(sequence)-(k-2):
    print(sequence[i:i+k-1])
    if sequence[i:i+(k-1)] not in adjacencyDictionary:
        adjacencyDictionary[sequence[i:i+(k-1)]] = {}  # add subsequence to dictionary, initialize it as empty dictionary
    j = i+1  # to make indices clearer: j is just the next (k-1)-let
    if len(sequence[i:]) > (k-1):  # if another subsequence exists after i
        if sequence[j:j+(k-1)] not in adjacencyDictionary[sequence[i:i+(k-1)]]:
            adjacencyDictionary[sequence[i:i+(k-1)]][sequence[j:j+(k-1)]] = 0  # if subsequence j follows subsequence i, then I want to add j to i's sub-dictionary
        adjacencyDictionary[sequence[i:i + (k - 1)]][sequence[j:j + (k - 1)]] = adjacencyDictionary[sequence[i:i+(k-1)]][sequence[j:j+(k-1)]] + 1
    i = j
print(adjacencyDictionary)
#"""
"""
testDict = {"CU": {"CU": 0, "UU": 1, "UG": 0},
            "UU": {"CU": 0, "UU": 2, "UG": 1},
            "UG": {"CU": 0, "UU": 0, "UG": 0}
            }
print(testDict)
print(testDict["UU"]["UU"])
teststring = "CUAG"
print(teststring[0:2] in testDict)
"""