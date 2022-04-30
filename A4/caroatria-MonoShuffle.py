#carolina atria

import random
import sys

def mono_shuffling(seq_string):
    list_of_nt=[]
    for i in seq_string:
        list_of_nt.append(i)
    length=len(seq_string)
    if length != 1:
        for j in range(length-1,0,-1): #going through from the back of the list
            switch_index=random.randrange(0,j,1)
            current_switch_nt = list_of_nt[j] #the position i am currently switching
            list_of_nt[j] = list_of_nt[switch_index]
            list_of_nt[switch_index] = current_switch_nt
    nt_permutations = ""
    for n in range(length):
        nt_permutations += list_of_nt[n]
    return(nt_permutations)
    
def string_reader():
    filename = sys.argv[3]
    with open(filename) as f:
        content = f.read().strip("\n")
        no_of_seq = int(sys.argv[2]) #number of permutations to print
        for n in range(no_of_seq):
            print(mono_shuffling(content))

string_reader()