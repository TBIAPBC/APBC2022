#-*- coding: utf-8 -*-
import sys
import re
doIgnore = False
doList = False 
argumentInput = len(sys.argv)
match argumentInput: 
    case 0: 
        print("Error")
    case 1: 
        print("No input file is given. Please enter a file name and retry")
    case 2: 
        inputFile = sys.argv[1]
    case 3: 
        inputFile = sys.argv[2] 
        if "I" in sys.argv[1]:
            doIgnore = True
        elif "l" in sys.argv[1]:
            doList = True
        else:
            print("No valid case is given.\n-I for ignoring upper/lowercase and -l printing a list of words.")
    case 4: 
        inputFile = sys.argv[3]
        if ("I" in sys.argv[1]) or ("I" in sys.argv[2]):
            doIgnore = True
            print("Iam here")
        if("l" in sys.argv[1]) or ("l" in sys.argv[2]):
            doList = True
        else:
            print("No valid case is given.\n-I for ignoring upper/lowercase and -l printing a list of words.")
     
#reading the input file
with open(inputFile, 'r', encoding="utf-8") as reader:
    inputText = reader.read()

if doIgnore:
    inputText = inputText.lower()

#splits the inputText into a list of words 
words = re.findall(r'[^\W_]+',inputText)

wordDict = dict()
for word in words:
    if word in wordDict:
        wordDict[word] += 1
    else:
        wordDict[word] = 1

if doList or doIgnore:    
    sortedKeys = sorted(wordDict.items(),key = lambda x: (-x[1],x[0]),reverse = False)
    for key in sortedKeys:
        print(str(key[0]) + "\t" + str(key[1]))
else:
    print(str(len(wordDict)) + "/" + str(len(words)))
    