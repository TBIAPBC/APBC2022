import sys
#checking if a input filename is given over the command line
if (len(sys.argv) > 1):
    inputFile = sys.argv[1]
else:
    inputFile = "HelloWorld-test1.in"
#reading the input file and trim the text
with open(inputFile, 'r') as reader:
    inputText = reader.read().strip()
#prints to standard output
print("Hello World!\n" + inputText)
    
  