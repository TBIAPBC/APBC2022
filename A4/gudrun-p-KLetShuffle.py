# created by Gudrun Poetzelberger
# on 10. April 2022

import random as rd
import sys

class Node:
    def __init__(self, sym, num, neighbours, seen, nextNum):
        self.sym = sym
        self.num = num
        self.neighbours = neighbours
        self.seen = seen
        self.nextNum = nextNum

    def printNode(self):  # useful for debugging
        print(self.sym, self.num, self.neighbours, self.seen, self.nextNum)

def createAdjacencyDic(sequence, k):
    adjacencyDictionary = {}  # I want to create a 2D dictionary "matrix", aka a dictionary of dictionaries,
    ## so that I can call things like adjacentDictionary['UU']['UC'], and the result is the number of edges 'UU'->'UC'
    ## I am using a dictionary and not an array or list because I need to be able to call it by key (subsequence-string, e.g. 'UC')
    i = 0
    while i < len(sequence) - (k - 2):
        #print(sequence[i:i + k - 1])
        if sequence[i:i + (k - 1)] not in adjacencyDictionary:
            adjacencyDictionary[sequence[i:i + (k - 1)]] = {}  # add subsequence to dictionary, initialize it as empty dictionary
        j = i + 1  # to make indices clearer: j is just the next (k-1)-let
        if len(sequence[i:]) > (k - 1):  # if another subsequence exists after i
            if sequence[j:j + (k - 1)] not in adjacencyDictionary[sequence[i:i + (k - 1)]]:
                adjacencyDictionary[sequence[i:i + (k - 1)]][
                    sequence[j:j + (k - 1)]] = 0  # if subsequence j follows subsequence i, then I want to add j to i's sub-dictionary
            adjacencyDictionary[sequence[i:i + (k - 1)]][sequence[j:j + (k - 1)]] = adjacencyDictionary[sequence[i:i + (k - 1)]][sequence[j:j + (k - 1)]] + 1
        i = j
    return adjacencyDictionary


def createMultigraph(adjDict):  # creates the data structure from the slides from an adjacency dictionary
    mulGraph = [None] * len(adjDict)  # list of same length as dictionary
    i = 0
    for km1let in adjDict:
        neighbours = getNeighboursList(adjDict, km1let)  # neighbours are symbols here, but I need numbers!
        ## But I only know the numbers after I have finished this for-loop to assign each subsequence-symbol a number
        mulGraph[i] = Node(km1let, i, neighbours, 0, None)
        i = i+1
    for k in range(0, len(mulGraph)):  # replace symbols of neighbours for numbers (id's)
        for p in range(0, len(mulGraph[k].neighbours)):
            for j in range(0, len(mulGraph)):
                if mulGraph[k].neighbours[p] == mulGraph[j].sym:
                    mulGraph[k].neighbours[p] = j
    return mulGraph

def getNeighboursList(adjDict, subsequence):
    neighbours = []
    for subseq, number in adjDict[subsequence].items():
        # print("subseq = ", subseq)
        # print("number = ", number)
        neighbours += [subseq] * number
    return neighbours

def findSpanningTree(mGraph):  # uses Wilson's algorithm
    root = mGraph[-1]  # root is the last subsequence
    current = mGraph[0]  # starting vertext is the first subsequence

    # if next is not None then erase loop


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

adjDict = createAdjacencyDic(sequence, k)
#
print(adjDict)
#print(getNeighboursList(adjDict, 'UA'))
multigraph = createMultigraph(adjDict)
#multigraph[2].printNode()
for node in multigraph:
    node.printNode()
print("random direction = ", rd.choice(multigraph[1].neighbours))




"""
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


adjDict = createAdjacencyDic(sequence, k)
print(adjDict)


#print(adjDict[0][0])
#print(len(adjDict))
#for se in adjDict:
#    print(se)
testlist = list(adjDict['UU'].keys())
print(testlist)

j=0
tlist = [None]*len(adjDict['UU'])
for neighbour in adjDict['UU']:
    tlist[j] = neighbour
    j = j + adjDict['UU'][neighbour]
print("tlist = ", tlist)

tlist = []
for subseq, number in adjDict['UU'].items():
    #print("subseq = ", subseq)
    #print("number = ", number)
    tlist += [subseq] * number

print(tlist)


testDict = {"CU": {"CU": 0, "UU": 1, "UG": 0},
            "UU": {"CU": 0, "UU": 2, "UG": 1},
            "UG": {"CU": 0, "UU": 0, "UG": 0}
            }
print(testDict)
print(testDict["UU"]["UU"])
teststring = "CUAG"
print(teststring[0:2] in testDict)
"""