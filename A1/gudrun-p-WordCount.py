import sys

list1 = False
ignore1 = False


args = sys.argv
#print("args = ", args)
assert len(args)>=2, "Both the python script and the text-input file must be provided!"

if len(args)>2:
    if '-l' in args:
        list1 = True
    if '-I' in args:
        ignore1 = True
    if len(args)==3:
        f = open(sys.argv[2], "r")
        original_text = f.read()
        f.close()
    if len(args)==4:
        f = open(sys.argv[3], "r")
        original_text = f.read()
        f.close()
else:
    f = open(sys.argv[1], "r")
    original_text = f.read()
    f.close()

#original_text = "hello I?!am-counting,hello---?I-I,I...Hello bee."  # for testing
text = ''.join(c  if c.isalnum() else " " for c in original_text)  # replace all non-alphanumeric characters with spaces
words = []
if ignore1:
    words = text.lower().split()
else:
    words = text.split()  # split strings into list of words, with space as seperator
myDict = {}
n = 0
for word in words:  # define dictionary with unique word as key and how often the word appears as value
    myDict[word] = words.count(word)  # e.g. if the word "hello" appears twice, then myDict[hello]=2
    n = n+1

sortedlist = sorted(myDict.items(), key=lambda x:(-x[1], x[0]))  # sort by frequency of words (minus to get most frequent first), then alphabetically


#print("Total Number of words: ", n)
#print("Number of different words: ", len(myDict))

if list1:
    for element in sortedlist:
        print("%s\t%s"%(element[0],element[1]))
else:
    print(len(myDict), '/', n)