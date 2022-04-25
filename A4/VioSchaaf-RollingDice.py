import sys
import numpy as np


filename = sys.argv[-1]
N = int(sys.argv[-2])
print(N)

file = open(filename, 'r')
file = file.readline()

#determine frequencies
A_count = 0
C_count = 0
G_count = 0
U_count = 0
total_count = 0

for letter in file:
    if letter == 'A':
        A_count += 1
        total_count += 1

    elif letter == 'C':
        C_count += 1
        total_count += 1

    elif letter == 'G':
        G_count += 1
        total_count += 1

    elif letter == 'U':
        U_count += 1
        total_count += 1


frequencies = [A_count/total_count, C_count/total_count, G_count/total_count, U_count/total_count]
freq_A = A_count/total_count
freq_C = C_count/total_count
freq_G = G_count/total_count
freq_U = U_count/total_count

nucleotides = ['A', 'C', 'G', 'U']
n = 0
while n < N:
    random_array = np.random.choice(nucleotides, size=total_count, p=frequencies)
    sequence = ""
    for element in random_array:
        sequence += element
    print(sequence)
    n += 1



