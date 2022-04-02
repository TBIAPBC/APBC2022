# A3 by Gudrun Pötzelberger, 00275117
# 1.4.2022

import sys

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
original_text = f.read()
f.close()

def readHVFile(file):
    print("to be implemented")