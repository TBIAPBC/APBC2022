#!/usr/bin/python
filename=input("Please input your filename: ")
f = open(filename, "r")
content = f.read()
print("Hello World!\n" + content, end="")