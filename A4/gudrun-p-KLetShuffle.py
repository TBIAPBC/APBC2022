# created by Gudrun Poetzelberger
# on 10. April 2022

import random as rd
import sys
import copy

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
        mulGraph[i] = Node(km1let, i, neighbours, False, None)
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

def findSpanningTree(multiGraph):  # uses Wilson's algorithm
    mGraph = copy.deepcopy(multiGraph)  # I want to keep the original multigraph, in order to be able to find multiple different spanning trees of it
    mGraph[-1].seen = True  # root is the last subsequence
    startNode = mGraph[0]  # starting vertext is the first subsequence
    currentNode = startNode
    unseenNodeExists = True
    while unseenNodeExists:
        while currentNode.seen == False:
            # delete loop (if loop was created):
            if currentNode.nextNum is not None:
                loopNode = currentNode
                currentNode = startNode
                while currentNode.num != loopNode.num:  # go along path until I get to the node that is later visited a second time (loopNode)
                    currentNode = mGraph[currentNode.nextNum]
                nextNodeNumber = currentNode.nextNum  # now currentNode is the loopNode
                currentNode.nextNum = None
                currentNode = mGraph[nextNodeNumber]
                while currentNode.num != loopNode.num:  # go along the loop until I visit loopNode a second time, and delete all next's
                    nextNodeNumber = currentNode.nextNum
                    currentNode.nextNum = None
                    currentNode = mGraph[nextNodeNumber]
            # Now loop is deleted, currentNode is loopNode again, and from here I again choose a random direction
            nextNodeNumber = rd.choice(currentNode.neighbours)  # choose a random neighbour of the current node
            currentNode.nextNum = nextNodeNumber
            currentNode = mGraph[nextNodeNumber]

        # if I have found a node that is already in the "seen" category: set all nodes on the path to "seen" as well
        seenNode = currentNode
        currentNode = startNode
        while currentNode.num != seenNode.num:  # go along path and set all to seen
            currentNode.seen = True
            currentNode = mGraph[currentNode.nextNum]
        # next start node:
        ## according to wikipedia (https://en.wikipedia.org/wiki/Maze_generation_algorithm):
        ## "This procedure remains unbiased no matter which method we use to arbitrarily choose starting cells.
        ## So we could always choose the first unfilled cell in (say) left-to-right, top-to-bottom order for simplicity."
        ## So I can just always choose the first unseen node in my multigraph datastructure
        unseenNodeExists = False
        for eachNode in mGraph:
            if eachNode.seen == False:
                eachNode.nextNum = None  # all nodes not on the path should not have a 'next'
                if unseenNodeExists ==False:  # define new start node
                    unseenNodeExists = True
                    startNode = eachNode
                    currentNode = startNode
    return mGraph


    # must .copy() so i keep multigraph


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

#print(multigraph[0].nextNum is not None)
#print("random direction = ", rd.choice(multigraph[1].neighbours))
spanningTree = findSpanningTree(multigraph)
print("")
for node in multigraph:
    node.printNode()
print("")
for node in spanningTree:
    node.printNode()




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