# created by Gudrun Poetzelberger
# on 10. April 2022

import random as rd
import sys

checkIfSameDistribution = False  # set to true to see the distribution before and after shuffling


def swapLetters(seqString, pos1, pos2):  # strings are immutable, so I have to create a new string
    spos1 = seqString[pos1]
    spos2 = seqString[pos2]  # so that function works no matter if pos1 or pos2 comes earlier
    newString = ''
    for k in range(0, len(seqString)):
        if k == pos1:
            newString = newString + spos2
        elif k == pos2:
            newString = newString + spos1
        else:
            newString = newString + seqString[k]
    return newString


def monoShuffle(seqString):
    sequenceLength = len(seqString)
    for i in range(0, sequenceLength):
        randomNumber = rd.randrange(i, sequenceLength)  # random integer number between [i,sequenceLength)
        seqString = swapLetters(seqString, i, randomNumber)
    return seqString


def countLetters(seqString):  # to check if code works correctly
    freqDict = {}  # frequency dictionary
    for letter in seqString:
        if letter not in freqDict:  # have to add letter before I can increase its frequency
            freqDict[letter] = 0
        freqDict[letter] = freqDict[letter] + 1  # letter's frequency increases by one
    return freqDict


args = sys.argv
assert len(args)==4, "Required program call format: gudrun-p-MonoShuffle.py -N 4 MonoShuffle-test1.in"
assert args[1] == "-N", "Required program call format: gudrun-p-MonoShuffle.py -N 4 MonoShuffle-test1.in"
N = int(args[-2])  # number of random sequences to be created
f = open(args[-1], "r")
sequence = f.read()
f.close()
if not sequence[-1].isalnum():  # remove the \n that is often at the end of the input files
    sequence = sequence[0:-1]

if checkIfSameDistribution:
    print("original distribution:")
    print(countLetters(sequence))

for i in range(0, N):
    shuffledSequence = monoShuffle(sequence)
    print(shuffledSequence)
    if checkIfSameDistribution:
        print("distribution after shuffling:")
        print(countLetters(shuffledSequence))