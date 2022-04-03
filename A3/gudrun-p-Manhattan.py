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


def maxPathHV(ns, ew):
    numberOfNodeRows = len(ew[:,0])
    numberOfNodeColumns = len(ns[0,:])
    MW = np.zeros([numberOfNodeRows, numberOfNodeColumns])
    for i in range(0, numberOfNodeRows):
        for j in range(0, numberOfNodeColumns):
            if i == 0 and j == 0:  # I am in the north-west corner (starting node). The maximum weight to get here is 0.
                MW[i,j] = 0
            elif i == 0:  # if I am in the north-most street, I can't have come from the north. I must have come from the west.
                MW[i,j] = MW[i,j-1] + ew[i,j-1]  # the maximum weight to get to node i,j-1 plus the weight to walk from j-1 to j
            elif j == 0:  # if I am in the west-most street, I must have come from the north.
                MW[i,j] = MW[i-1,j] + ns[i-1,j]  # maximum weight to get to node (i-1,j) plus the weight to walk to node (i,j) from the north.
            else:  # to get to node (i,j) I can either come from the north or from the east.
                # I want to have come from the node that has the maximum (weight to get to it + weight to get from it to (i,j)).
                MW[i,j] = max(MW[i,j-1] + ew[i,j-1], MW[i-1,j] + ns[i-1,j])  # result: maximum weight to get to node (i,j)
    return MW[numberOfNodeRows-1, numberOfNodeColumns-1]








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


maxpath = maxPathHV(ns, ew)
print(maxpath)

