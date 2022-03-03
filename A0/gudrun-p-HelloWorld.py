import sys

f = open(sys.argv[1], "r")
contents = f.read()
f.close()
print("Hello World!")
print(contents, end="")