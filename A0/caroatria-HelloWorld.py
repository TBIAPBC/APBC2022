#!/usr/bin/python
import sys
filename=sys.argv[1]
f = open(filename, "r")
content = f.read()
print("Hello World!\n" + content, end="")