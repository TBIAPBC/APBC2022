# A3 by Gudrun Pötzelberger, 00275117
# 1.4.2022
import sys
import numpy as np

def readHVFile(file):
    ns = []
    ew = []
    firstline = True
    lines = f.readlines()
    nsColumns = 0
    for line in lines:
        if line[0] != '#':
            row = line.split()
            if len(row) != 0:
                row = [float(i) for i in row]
                if firstline:
                    nsColumns = len(row)
                firstline = False
                if len(row) < nsColumns:
                    ew.append(row)
                else:
                    ns.append(row)
    return ns, ew

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

"""
print("ns = ", ns)
print("ew = ", ew)
print("ns[1][1] = ", ns[1][2])
print("ew[1][1] = ", ew[2][1])
print("npparray(ns) = ", np.array(ns))
"""


