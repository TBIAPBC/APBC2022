import sys, getopt

list1 = False
ignore1 = False


args = sys.argv
print("args = ", args)
assert len(args)>=2, "Both the python script and the text-input file must be provided!"

if len(args)>2:
    if '-l' in args:
        list1 = True
    if '-I' in args:
        ignore1 = True

#f = open(sys.argv[1], "r")
#original_text = f.read()
#f.close()



#opts, args = getopt.getopt(sys.argv[1:], "l:I")
#print("args = ", args)
#print("opts = ",opts)

original_text = "hello I?!am-counting,hello---?I-I,I"
text = ''.join(c  if c.isalnum() else " " for c in original_text)  # replace all non-alphanumeric characters with spaces
words = []
words = text.split() # or string.lower().split()  # split strings into list of words, with space as seperator
myDict = {}
n = 0
for word in words:  # define dictionary with unique word as key and how often the word appears as value
    myDict[word] = words.count(word)  # e.g. if the word "hello" appears twice, then myDict[hello]=2
    n = n+1

sortedlist = sorted(myDict.items(), key=lambda x:x[1], reverse=True)  # not sure it is necessary, but in the example output, it is sorted by frequency of words

#print(original_text)
#print(text)
#print("Dictionary Items  :  ",  myDict)
print("Total Number of words: ", n)
print("Number of different words: ", len(myDict))
print(sortedlist)