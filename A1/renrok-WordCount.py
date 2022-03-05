import sys
import re

#reading the input file
def getInputText(inputFile):
    with open(inputFile, 'r', encoding="utf-8") as reader:
        inputText = reader.read()
    return inputText

def main():
    doIgnore = False
    doList = False 
    match len(sys.argv): 
        case 1: 
            print("No input file is given. Please enter a file name after the scriptname and retry")
            exit()
        case 2: 
            inputText = getInputText(sys.argv[1])
        case 3: 
            inputText = getInputText(sys.argv[2])       
            if "I" in sys.argv[1]:
                doIgnore = True
            elif "l" in sys.argv[1]:
                doList = True
        case 4: 
            inputText = getInputText(sys.argv[3])
            if ("I" in sys.argv[1]) | ("I" in sys.argv[2]):
                doIgnore = True  
            if("l" in sys.argv[1]) | ("l" in sys.argv[2]):
                doList = True            

    #converting all upper case to lower case if -I is present in sys argument
    if doIgnore:
        inputText = inputText.lower()

    #splits the inputText into a list of words 
    words = re.findall(r'[^\W_]+',inputText)

    #count words
    wordDict = dict()
    for word in words:
        if word in wordDict:
            wordDict[word] += 1
        else:
            wordDict[word] = 1

    #if -l is present in sys argument prints a list otherwise number of words is printed
    if doList: 
        sortedKeys = sorted(wordDict.items(),key = lambda x: (-x[1],x[0]),reverse = False)
        for key in sortedKeys:
            print(f"{(key[0])}\t{(key[1])}")
    else:
          print(f"{len(wordDict)} / {len(words)}")
      
if __name__ == '__main__':
    main()