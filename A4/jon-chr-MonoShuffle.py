import os
import sys
import random
from random import randint

# Implement MonoShuffle, inspired by Fisher-Yates Shuffling
def monoshuffle(sequence):
    seq = [i for i in sequence]
    # Else no shuffling necessary
    n = len(seq)
    if n > 2:
         for i in range(n-1, 0, -1):
                rand = randint(0,i+1)
                new_r = seq[rand]
                new_i = seq[i]
                seq[i] = new_r
                seq[rand] = new_i
    res = ""
    for i in range(n):
        res += seq[i]
                
    return res 

### Main
seq = ""
file = sys.argv[1]

f = open(file)
for line in f:
    seq = line.strip()
f.close()  

new_seq = monoshuffle(seq)
print(new_seq)

