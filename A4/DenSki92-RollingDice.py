import sys
from random import random
arr = []

with open(sys.argv[3], "r") as df:
    for line in df:
        arr.append(line.strip("\n"))

ORDER = "ACGU"

N = int(sys.argv[2])
count_n =  [0,0,0,0]

for n in arr[0]:
    if n == "G":
        count_n[2] += 1
    elif n == "A":
        count_n[0] += 1
    elif n == "C":
        count_n[1] += 1
    elif n == "U":
        count_n[3] += 1
    else:
        print(f"{n} is unknown!")

count_sum = sum(count_n)

prob_n = [x/count_sum for x in count_n]

for i in range(N):
    rand_seq = ""
    for i in range(count_sum):
        rand_num = random()
        if rand_num <= prob_n[0]:
            rand_seq += "A"
        elif rand_num <= prob_n[0] + prob_n[1]:
            rand_seq += "C"
        elif rand_num <= 1 - prob_n[3]:
            rand_seq += "G"
        elif rand_num <= 1:
            rand_seq += "U"

    print(rand_seq)
