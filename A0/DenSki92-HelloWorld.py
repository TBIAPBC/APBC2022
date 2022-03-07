import sys

with open(sys.argv[1], "r") as r_file:
    text = r_file.read()

print("Hello World\n" + text)
