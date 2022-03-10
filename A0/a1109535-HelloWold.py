import sys #library to use cl arguments

with open (sys.argv[1],'r') as content:
    print("Hello World!")
    print(content.read())

