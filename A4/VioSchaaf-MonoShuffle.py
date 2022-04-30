import sys
import numpy as np

def swap(file):
    for i in range(len(file) - 1):
        n = np.random.choice(list(range(i + 1, len(file))))

        x = file[i]
        file[i] = file[n]
        file[n] = x
        sequence = ''.join(file)

    return sequence


filename = sys.argv[-1]
N = int(sys.argv[-2])
print(N)

file = open(filename, 'r')
file = list(file.readline().strip())

count = 0
while count < N:
    print(swap(file))
    count += 1


