import sys
#checking if a input filename is given over the command line
if (len(sys.argv) > 1):
    inputFile = sys.argv[1]
else:
    inputFile = "HelloWorld-test1.in"
#reading the input file and trim the text
with open(inputFile, 'r') as reader:
    inputText = reader.read().strip()
#writing into the output file with additionally Hello World
with open('HelloWorld-test1.out', 'w') as writer:
    writer.write("Hello World!\n" + inputText)
#prints output to standard output
print("Hello World!\n" + inputText)