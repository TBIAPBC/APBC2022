import sys


#clemensheiderer-HelloWorld.py HelloWorld-test1.in

def read(thatandmore):
    with open(thatandmore, 'r') as f:
        for line in f:
            return line.strip()


text = read(sys.argv[1])
#

outprint_world = "Hello World!\n" + str(text)
#sys.stdout = open('HelloWorld-test1.out','wt')

print(outprint_world)
