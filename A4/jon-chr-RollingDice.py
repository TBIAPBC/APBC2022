import os
import sys
import random

# Rolling Dice 
def freq_string(string):
    freq = {}
    length = 0 
    # Determine frequencies of Symbols in String
    for symbol in string:
        length += 1
        if symbol in freq:
            freq[symbol] += 1
        else:
            freq[symbol] = 1
    # Isolate total frequencies and symbols
    symbols = freq.keys()
    total_freq = sum(freq.values())
    assert total_freq == length 
    
    # Calculate freq. in probabilities
    for i in symbols:
        freq[i] = round((freq[i] / total_freq), 1)
    tot_freq = round((sum(freq.values())),1)
    assert tot_freq == 1
    
    return freq, length 


def draw_symbols(freq, length, N):
    symbols = list(freq.keys())
    prob = list(freq.values())
    sequences = []
    for count in range(N):
        res = ""
        for i in range(length):
            letter = random.choices(symbols, prob)
            res += letter[0]
        sequences.append(res)
    return sequences
    

### Main

# Command-line
file = ""
N = 0

for cmd in sys.argv:
    if isinstance(cmd, int):
        N = cmd
    elif cmd.lower() == "-n":
        continue
    else:
        file = cmd 
        
# Read-in file
f = open(file)
for line in f:
    string = line.strip()
f.close()

# Task
freq, l = freq_string(string)
sequences = draw_symbols(freq, l, N)

# Print to console
for s in sequences:
    print(s)

