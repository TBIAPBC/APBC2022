# A3 by Gudrun Pötzelberger, 00275117
# 1.4.2022
import sys
import numpy as np

def readHVFile(file):
    ns = []  # list of weights of all north-south streets
    ew = []  # list of weights of all east-west streets
    firstline = True  # use this to set the number of columns of north-south streets
    lines = file.readlines()  # read each line separately so I can ignore those that are comments
    nsColumns = 0  # number of columns of north-south streets
    for line in lines:
        if line[0] != '#':  # ignore lines that are comments
            row = line.split()  # split by spaces so each number is separate
            if len(row) != 0:  # ignore empty lines
                row = [float(i) for i in row]  # convert all numbers from strings to ints
                if firstline:  # only the first line that isnt empty and isnt a comment
                    nsColumns = len(row)  # set number of north-south streets so I know when the east-west streets start
                firstline = False
                if len(row) < nsColumns:  # all these lines are east-west streets
                    ew.append(row)
                else:  # all these lines are north-south streets
                    ns.append(row)
    return np.array(ns), np.array(ew)  # return numpy arrays (more pleasant to work with)


def maxWeightHV(ns, ew):  # calculates the weight of the maximum weight path from the starting node to the target node
    numberOfNodeRows = len(ew[:,0])
    numberOfNodeColumns = len(ns[0,:])
    MW = np.zeros([numberOfNodeRows, numberOfNodeColumns])  # MW(i,j) = weight of maximum weight path that leads to node (i,j)
    for i in np.arange(0, numberOfNodeRows):
        for j in np.arange(0, numberOfNodeColumns):
            if i == 0 and j == 0:  # I am in the north-west corner (starting node). The maximum weight to get here is 0.
                MW[i,j] = 0
            elif i == 0:  # if I am in the north-most street, I can't have come from the north. I must have come from the west.
                MW[i,j] = MW[i,j-1] + ew[i,j-1]  # the maximum weight to get to node i,j-1 plus the weight to walk from j-1 to j
            elif j == 0:  # if I am in the west-most street, I must have come from the north.
                MW[i,j] = MW[i-1,j] + ns[i-1,j]  # maximum weight to get to node (i-1,j) plus the weight to walk to node (i,j) from the north.
            else:  # to get to node (i,j) I can either come from the north or from the east.
                # I want to have come from the node that has the maximum (weight to get to it + weight to get from it to (i,j)).
                MW[i,j] = max(MW[i,j-1] + ew[i,j-1], MW[i-1,j] + ns[i-1,j])  # result: maximum weight to get to node (i,j)
    return MW[numberOfNodeRows-1, numberOfNodeColumns-1]  # return last entry of MW matrix (bottom right, target node)


def maxPathHV(ns, ew):  # calculates the weight of the maximum weight path and the maximum weight path from the starting node to the target node
    numberOfNodeRows = len(ew[:,0])
    numberOfNodeColumns = len(ns[0,:])
    MW = np.zeros([numberOfNodeRows, numberOfNodeColumns])  # MW(i,j) = weight of maximum weight path that leads to node (i,j)
    CameFrom = np.empty([numberOfNodeRows, numberOfNodeColumns], dtype="<U1")  # string matrix that saves heaviest path to each node (i,j) but backwards (where you came from)
    for i in np.arange(0, numberOfNodeRows):
        for j in np.arange(0, numberOfNodeColumns):
            if i == 0 and j == 0:  # I am in the north-west corner (starting node). The maximum weight to get here is 0.
                MW[i,j] = 0
            elif i == 0:  # if I am in the north-most street, I can't have come from the north. I must have come from the west.
                MW[i,j] = MW[i,j-1] + ew[i,j-1]  # the maximum weight to get to node i,j-1 plus the weight to walk from j-1 to j
                CameFrom[i,j] = 'W'  # I came from the west to get to (i,j)
            elif j == 0:  # if I am in the west-most street, I must have come from the north.
                MW[i,j] = MW[i-1,j] + ns[i-1,j]  # maximum weight to get to node (i-1,j) plus the weight to walk to node (i,j) from the north.
                CameFrom[i,j] = 'N'  # I came from the north to get to (i,j)
            else:  # to get to node (i,j) I can either come from the north or from the east.
                # I want to have come from the node that has the maximum (weight to get to it + weight to get from it to (i,j)).
                if MW[i,j-1] + ew[i,j-1] > MW[i-1,j] + ns[i-1,j]:  # Heavier path if I came from the west
                    MW[i,j] = MW[i,j-1] + ew[i,j-1]
                    CameFrom[i,j] = 'W'
                else:  # heavier path if I came from the north (or if the two paths are equal)
                    MW[i,j] = MW[i - 1, j] + ns[i - 1, j]
                    CameFrom[i,j] = 'N'
    MaximumPathWeight = MW[numberOfNodeRows-1, numberOfNodeColumns-1]
    numberOfSteps = numberOfNodeRows + numberOfNodeColumns - 2  # number of steps needed to go from starting node to target node (independent of path)
    backwardsPath = np.empty(numberOfSteps, dtype="<U1")  # vector of length number-of-steps that are needed to reach target node
    i = numberOfNodeRows-1
    j = numberOfNodeColumns-1
    k = 0
    while k < numberOfSteps:
        backwardsPath[k] = CameFrom[i, j]
        if backwardsPath[k] == 'N':  # if I came to the node from the north, next look at the node to the north
            i = i-1
        elif backwardsPath[k] == 'W':  # if I came from the west, look how I got to the node in the west
            j = j-1
        k = k+1
    path = np.empty(numberOfSteps, dtype="<U1")
    for i in np.arange(0, numberOfSteps):
        if backwardsPath[numberOfSteps-1-i] == 'N':  # start with last element of backwardsPath, which is how I got from starting node to next node
            path[i] = 'S'
        if backwardsPath[
            numberOfSteps - 1 - i] == 'W':
            path[i] = 'E'
    # I could have used 'S' and 'E' from the start instead of 'W' and 'N', then I would just have to reverse the backwardsPath vector
    # However, I find that the concept of what is being calculated is more easy to understand by using 'N' and 'W'.
    # I depends if performance or understandability is more important.
    return MaximumPathWeight, path






diagonalFile = False
printBestPath = False

args = sys.argv
#print("args = ", args)
assert len(args)>=2, "Both the python script and the text-input file must be provided!"
if len(args)>2:
    if '-d' in args:
        diagonalFile = True
    if '-t' in args:
        printBestPath = True
f = open(sys.argv[-1], "r")
if not diagonalFile:
    [ns, ew] = readHVFile(f)
else:
    print("diagonal file reading not yet implemented")
f.close()


#print("ns = ", ns)
#print("ew = ", ew)
#print("ns[1][1] = ", ns[1][2])
#print("ew[1][1] = ", ew[2][1])
#print("npparray(ns) = ", np.array(ns))



if printBestPath:
    [maxweight, maxpath] = maxPathHV(ns, ew)
    print(maxweight)
    for p in maxpath:
        print(p, end="")
else:
    maxweight = maxWeightHV(ns, ew)
    print(maxweight)