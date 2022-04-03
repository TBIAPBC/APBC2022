import math
import sys

import numpy


def readInputFile(inputFile):
    with open(inputFile, 'r', encoding="utf-8") as reader:
        inputText = reader.readlines()

    # get the values for the matrix
    coordinates = []
    for line in inputText:
        if ('#' not in line) & (len(line.strip()) > 0):  # ignore comments line an empty lines
            coordinates.append(line.split())

    # get dimension of the matrix
    northSouthValues = []
    westEastValues = []
    for line in coordinates:
        if len(line) < len(coordinates[0]):
            line = [float(x) for x in line]
            westEastValues.append(line)
        else:
            line = [float(x) for x in line]
            northSouthValues.append(line)

    # check if there are also diagonal values
    if len(westEastValues) > len(northSouthValues[0]):
        diagonals = westEastValues[len(northSouthValues[0]):]
        westEastValues = westEastValues[:len(northSouthValues[0])]
        return numpy.array(northSouthValues), numpy.array(westEastValues), numpy.array(diagonals)

    return numpy.array(northSouthValues), numpy.array(westEastValues), numpy.empty(0)


# calculate the solution matrix (D) with the levenshtein recursive formula with the given distances (northSouth,
# westEast and diagonals)
def calculateMatrix(northSouth, westEast, diagonals, doDiagonal):
    # init zero matrix - D_0_0 = 0
    D = numpy.zeros([westEast.shape[0], northSouth.shape[1]])

    # add values for D_i_0 = sum i vertical distances | i > 0 since D_0_0 = 0
    for i in range(1, D.shape[0]):
        D[i, 0] = D[i - 1, 0] + northSouth[i - 1, 0]

    # add values for D_0_j = sum j horizontal distances | j > 0 since D_0_0 = 0
    for j in range(1, D.shape[1]):
        D[0, j] = D[0, j - 1] + westEast[0, j - 1]

    # calculate remaining values by starting with D_1_1 and always take the maximum value
    currentValue = 0
    for i in range(1, D.shape[0]):
        for j in range(1, D.shape[1]):
            southStep = D[i - 1, j] + northSouth[i - 1, j]  # one step south
            eastStep = D[i, j - 1] + westEast[i, j - 1]  # one step east
            if doDiagonal & numpy.any(diagonals):
                diagonalStep = D[i - 1, j - 1] + diagonals[i - 1, j - 1]  # one diagonal (left-right) step
                D[i, j] = max(diagonalStep, southStep, eastStep)
            else:
                D[i, j] = max(southStep, eastStep)

        currentValue = D[i, j]
    return D, currentValue


def findPath(D, northSouth, westEast, diagonals, doDiagonal):
    i = D.shape[0] - 1
    j = D.shape[1] - 1
    path = ''
    while True:
        southStep = D[i - 1, j] + northSouth[i - 1, j]
        eastStep = D[i, j - 1] + westEast[i, j - 1]
        if doDiagonal & diagonals.any():
            diagonalStep = D[i - 1, j - 1] + diagonals[i - 1, j - 1]
        else:
            diagonalStep = math.inf

        # traceback the steps that have been made to receive the path
        if D[i, j] == southStep:
            path = 'S' + path
            i -= 1  # one step north
        elif D[i, j] == eastStep:
            path = 'E' + path
            j -= 1  # one step west
        elif D[i, j] == diagonalStep:
            path = 'D' + path
            i -= 1  # one diagonal (right-left) step
            j -= 1

        # terminates when the position D_0_0 is reached
        if (i == 0) & (j == 0):
            return path


def main():
    doDiagonal = False
    doPrintPath = False
    inputFile = ''
    match len(sys.argv):
        case 1:
            print("No input file is given. Please enter a file name after the scriptname and retry")
            exit()
        case 2:
            inputFile = sys.argv[1]
        case 3:
            inputFile = sys.argv[2]
            if "d" in sys.argv[1]:
                doDiagonal = True
            elif "t" in sys.argv[1]:
                doPrintPath = True
        case 4:
            inputFile = sys.argv[3]
            if ("d" in sys.argv[1]) | ("d" in sys.argv[2]):
                doDiagonal = True
            if ("t" in sys.argv[1]) | ("t" in sys.argv[2]):
                doPrintPath = True

    northSouth, westEast, diagonals = readInputFile(inputFile)
    D, bestValue = calculateMatrix(northSouth, westEast, diagonals, doDiagonal)
    print(bestValue)

    if doPrintPath:
        path = findPath(D, northSouth, westEast, diagonals, doDiagonal)
        print(path)


if __name__ == '__main__':
    main()
