import itertools
import re
import sys


# reading the input file and get a list with each line in it.
def getInputText(inputFile):
    with open(inputFile, 'r', encoding="utf-8") as reader:
        inputText = reader.readlines()
    return inputText


class Node:
    def __init__(self, name, cost):
        self.name = name
        self.cost = cost


# checks if the potentialNode or a permutation of it is already in the solution List
def isEqual(solutionList, potentialNode):
    for item in solutionList:
        if (item.name.find(potentialNode.name[0]) != -1) | (item.name.find(potentialNode.name[1]) != -1):
            return False
    return True


# returns the cost of a potentialNode the solutionList
def getCurrentCost(solutionList, potentialNodeCost):
    cost = potentialNodeCost
    for node in solutionList:
        cost += node.cost
    return cost


# checks if the currentSolution is already in the solution to avoid duplicates
def duplicate(solution):
    if len(globalSolution) == 0:
        return False
    possibleSolutions = list(itertools.permutations(solution))
    for current in globalSolution:
        for possibilities in possibleSolutions:
            if current.name.find(getString(possibilities)) != -1:  # true if value is found
                return True
    return False


def getString(solution):
    resultString = ''
    for node in solution:
        resultString += node.name + " "
    resultString.strip()
    return resultString


def branchAndBound(authoritiesList, solution):
    global costLimit
    # termination condition
    if (len(authoritiesList) == 0) | (authoritiesList is None):
        return solution

    if len(solution) == numberCapitals / 2:
        stringSolution = getString(solution)
        if not duplicate(solution):
            solutionCost = getCurrentCost(solution, 0)
            globalSolution.append(Node(stringSolution, solutionCost))

    count = 0
    for potentialAuthority in authoritiesList:
        count += 1
        if isEqual(solution, potentialAuthority):
            currentCost = getCurrentCost(solution, potentialAuthority.cost)
            if currentCost <= costLimit:
                tempSolution = solution.copy()
                tempSolution.append(potentialAuthority)
                branchAndBound(authoritiesList[count:].copy(), tempSolution)
    return solution


def getBestSolution(globalSolution):
    bestSolution = Node('inf', 1000000)
    for solution in globalSolution:
        if solution.cost < bestSolution.cost:
            bestSolution = solution
    return bestSolution


def main():
    global costLimit, numberCapitals, globalSolution, optimize
    optimize = False
    match len(sys.argv):
        case 1:
            print("No input file is given. Please enter a file name after the scriptname and retry")
            exit()
        case 2:
            inputText = getInputText(sys.argv[1])
        case 3:
            inputText = getInputText(sys.argv[1])
            if "o" in sys.argv[2]:
                optimize = True

    globalSolution = []
    numberCapitals = int(inputText[0].split(" ")[0].strip())
    costLimit = int(inputText[0].split(" ")[1].strip())
    capitals = re.findall(r'[^\W_]+', inputText[1])
    costs = re.findall(r'[^\n|^" "]+', ''.join(inputText[2:]))

    nodeList = []
    for i in range(0, numberCapitals, 1):
        for j in range(0, numberCapitals, 1):
            if (j is not i) & (i < j):
                nodeCost = int(costs[(i * numberCapitals) + j])
                nodeName = capitals[i] + capitals[j]
                nodeList.append(Node(nodeName, nodeCost))

    branchAndBound(nodeList, [])
    if optimize:
        best = getBestSolution(globalSolution)
        print(f'{best.name}')
    else:
        for solution in globalSolution:
            print(f'{solution.name}')

if __name__ == '__main__':
    main()
