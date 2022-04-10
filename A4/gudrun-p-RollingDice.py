#  created by Gudrun Poetzelberger
#  on 10.April 2022

import random as rd
import sys


def chooseRandomLetter(sortedProbabilityList):  # draw one letter according to the input sequence probability distribution
    randomNumber = rd.random()  # random number between 0 and 1
    probability = 0
    for element in sortedProbabilityList:
        probability = probability + element[1]
        if randomNumber < probability:
            return element[0]


def createRandomSequence(sortedProbabilityList, sequenceLength):  # create a random sequence of the same length as the input sequence with the same probability distribution
    seq = [None] * sequenceLength  # initialize list of sequenceLength
    i = 0
    while i < sequenceLength:
        seq[i] = chooseRandomLetter(sortedProbabilityList)
        i = i+1
    return seq


def printSequence(seq):  # this function makes it easier to print a sequence in the desired format
    for letter in seq:
        print(letter, end="")


args = sys.argv
assert len(args)==4, "Required program call format: gudrun-p-RollingDice.py -N 4 RollingDice-test1.in"
assert args[1] == "-N", "Required program call format: gudrun-p-RollingDice.py -N 4 RollingDice-test1.in"
N = int(args[-2])  # number of random sequences to be created
f = open(args[-1], "r")
sequence = f.read()
f.close()

freqDict = {}  # frequency dictionary
for letter in sequence:
    if letter.isalnum():  # filter out \n and similar special characters
        if letter not in freqDict:  # have to add letter before I can increase its frequency
            freqDict[letter] = 0
        freqDict[letter] = freqDict[letter] + 1  # letter's frequency increases by one

seqLength = sum(freqDict.values())  # length of the input sequence
for letter in freqDict.keys():
    freqDict[letter] = freqDict[letter]/seqLength  # to get from absolute number of appearances to probabilities
sortedProb = sorted(freqDict.items(), key=lambda x:(x[1]))  # create sorted list of tuples, sort by probability of letters (ascending)

for j in range(0, N):
    s = createRandomSequence(sortedProb, seqLength)
    printSequence(s)
    print("")  # newline
