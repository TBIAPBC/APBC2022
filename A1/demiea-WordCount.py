#!/usr/bin/env python3
import sys
import re

# get filename and open it
filename = sys.argv[1]
open_file = open(filename)

# create bools for arguments and set false
get_list = False
get_lower = False

# bool = true if entered in commandline
for i in range(len(sys.argv)):
    if sys.argv[i] == "-l":
        get_list = True
    if sys.argv[i] == "-I":
        get_lower = True

# read through lines and replace symbols with spaces and store words into list "file_new"
data = open_file.readlines()
regex = re.compile('[^a-zA-ZäöüÄÖÜß]', flags=re.UNICODE)
file_new = []
for sym in data:
    data_new = regex.sub(' ', sym)
    words_new = data_new.split()

    # store words in list
    for w in words_new:
        file_new.append(w)

# if bool "get_lower" is true => entered via command line
if get_lower:
    for lo in range(len(file_new)):
        file_new[lo] = file_new[lo].lower()

occurences = []
for words in file_new:
    count = 0
    if words not in occurences:
        occurences.append(words)

# if no additional arguments are given
if get_list == False and get_lower == False:
    print(len(occurences), "/", len(file_new))

# if bool "get_list" is true => entered via command line
if get_list:
    # create dictionarys
    dictionary = {}
    d = dict()

    # Iterate over each word in line
    for word in file_new:

        # Check if the word is already in dictionary
        if word in d:
            # Increment count of word by 1
            d[word] = d[word] + 1
        else:
            # Add the word to dictionary with count 1
            d[word] = 1

        dictionary[word] = d[word]

    # Print the contents of dictionary
    words_sorted = sorted(dictionary.items(), key=lambda x: x[1], reverse=True)
    for keys in words_sorted:
        print(keys[0], ":", keys[1])
