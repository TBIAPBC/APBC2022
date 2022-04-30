import random
import sys

def input_verifier():
    if len(sys.argv) != 4:
        print("Please provide the correct arguments! \n  file.py -N [int] input_file.%txt")
   ## make sure that the file name is in the last position  
    elif len(sys.argv)>2 and (sys.argv[-1].isdigit() or (sys.argv[-1] == "-N")):
        print("Please provide the correct arguments! \n  file.py -N [int] input_file.%txt")
    else:
        return True


### splits sequence into characters and makes a list, so the program can swap the elements later
def get_sequence(file):
    with open(file,"r") as input:
        seq = input.readline().strip()

    char_list = []
    for el in seq:
        char_list.append(el)
    return char_list

def swap(seq, old, new):
    current = seq[old]
    seq[old] = seq[new]
    seq[new] = current
    return seq

def monoshuffle(seq):
    for i in range(0, len(seq)-1):
        new_index = random.randint(i, len(seq)-1)
        seq = swap(seq, i, new_index)
    return "".join(seq)

if __name__ == "__main__":

    if input_verifier():

        ### input
        arguments = sys.argv
        file_name = arguments[-1]
        N = int(arguments[arguments.index("-N")+1])

        sequence = get_sequence(file_name)

        for i in range(N):
            print(monoshuffle(sequence))