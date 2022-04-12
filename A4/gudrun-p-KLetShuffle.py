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


def shuffleList(theList, lastEntry):  # shuffle a list using Fisher-Yates shuffling, with a non-random chosen last entry
    for i in range(0, len(theList)):  # put lastEntry at the end of the list
        if theList[i] == lastEntry:
            swapListElements(theList, i, -1)
            break
    for j in range(0, len(theList)-1):
        randomInteger = rd.randrange(j, len(theList)-1)
        swapListElements(theList, j, randomInteger)
    return theList

def swapListElements(theList, index1, index2):
    temp = theList[index1]
    theList[index1] = theList[index2]
    theList[index2] = temp


def generateSequence(sTree):  # takes a spanning tree multigraph where the neighbours have already been shuffled,
    ## and returns a random sequence that preserves k-let frequencies of the original sequence
    seq = [sTree[0].num]
    neighboursExist = True
    while neighboursExist == True:
        while sTree[seq[-1]].neighbours != []:  # until we get sent to a node that does not have any neighbours
            seq = seq + [sTree[seq[-1]].neighbours[0]]  # add the neighbour of the previous node to the sequence
            del sTree[seq[-2]].neighbours[0]  # delete the neighbour that was just added from the neighbours-list
            #for eachNode in sTree:
            #    eachNode.printNode()
            #print("")
        neighboursExist = False  # we got sent to a node without neighbours. 
        for eachNode in sTree:  # Check if a different node still has neighbours
            if eachNode.neighbours != []:
                neighboursExist = True
                seq = seq + [eachNode.neighbours[0]]  # if a node still has neighbours, we add the first neighbour to the sequence
                del sTree[eachNode.num].neighbours[0]  # delete that neighbour from the list
                break  # and go on with the algorithm, using this new node as a new starting point.
    return seq


#rd.seed(42)  # random seed to make results reproducible
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

#sequence3 = "CUUUUGCUAG"  # for testing
#sequence2 = "CUUUUGCUAGCUGCCUUGCUUA"  # for testing
#sequence1 = "ABCD"  # for testing
#sequence = "ABDBJAD"  # ABDBJAD with seed(42)
#k = 2  # for testing

for q in range(0, N):
    adjDict = createAdjacencyDic(sequence, k)
    multigraph = createMultigraph(adjDict)
    spanningTree = findSpanningTree(multigraph)
    for i in range(0, len(spanningTree)):
        shuffleList(spanningTree[i].neighbours, spanningTree[i].nextNum)  # shuffle all neighbours and make the 'next' subsequence the 'last' neighbour
    """
    print("spanning Tree:")
    for node in spanningTree:
        node.printNode()
    print("end spanning Tree")
    """
    newSequence = generateSequence(spanningTree)
    #print(newSequence)
    #print(sequence)
    
    # print resulting sequence:
    print(spanningTree[0].sym, end="")
    for zahl in newSequence[1:]:
        print(spanningTree[zahl].sym[-1], end="")
    print("")
