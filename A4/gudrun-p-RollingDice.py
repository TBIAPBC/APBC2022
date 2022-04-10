#  created by Gudrun Poetzelberger
#  on 10.April 2022

import random as rd
import sys

args = sys.argv
assert len(args)==2, "Exactly two files must be provided: the python script and the text-input file."
f = open(args[1], "r")
sequence = f.read()
f.close()

freqDict = {}  # frequency dictionary
for letter in sequence:
    if letter.isalnum():  # filter out \n and similar special characters
        if letter not in freqDict:  # have to add letter before I can increase its frequency
            freqDict[letter] = 0
        freqDict[letter] = freqDict[letter] + 1  # letter's frequency increases by one
print(freqDict)
