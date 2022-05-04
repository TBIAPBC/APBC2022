import argparse
from random import randint


parser = argparse.ArgumentParser()
parser.add_argument("file_name", help="a file to read")
args = parser.parse_args()

arr = []
with open(args.file_name, "r") as df:
    for line in df:
        arr.append(line.strip("\n"))


seq_used = arr[0]
for i in range(len(seq_used)-1):
    current_n = seq_used[i]
    rand_pos = randint(i+1, len(seq_used)-1)
    selected_n = seq_used[rand_pos]
    seq_used = seq_used[:i] + selected_n + seq_used[i+1:]
    seq_used = seq_used[:rand_pos] + current_n + seq_used[rand_pos+1:]

print(seq_used)
