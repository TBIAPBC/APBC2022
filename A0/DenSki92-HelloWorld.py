import sys

with open(sys.argv[1], "r") as r_file:
    text = r_file.read()

print("Hello World\n" + text)


#with open("HelloWorld-test1.out", "w") as w_file:
#    w_file.write("Hello World\n")
#    w_file.write(text)

