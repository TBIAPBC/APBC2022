import sys
import numpy as np
import pandas as pd

def shuffle_loop(loop, sequence, k):
    """
    finds a klet within the loop at which the loop sequence can be integrated into the main sequence
    :param loop: loop sequence
    :param sequence: main sequence
    :param k: klet length
    :return: new loop sequence
    """
    for i in range(len(loop)-k+1):
        loop_klet = loop[i:i+k-1]

        for j in range(len(sequence)-k):
            seq_klet = sequence[j:j+k-1]
            if loop_klet == seq_klet:

                new_loop = loop[i:] + loop[k-1:i+k-1]

                return new_loop


def shuffle(neighbours_dict, start):
    """
    Function which shuffles klets randomly starting from a given start
    :param neighbours_dict: dictionary containing all neighbours for each klet
    :param start: start element
    :return: shuffled sequence(s)
    """

    i = start
    all_sequences = []
    sequence = i[:k - 2]

    new_i = []
    for key in neighbours_dict:
        if neighbours_dict[key]:
            new_i.append(key)

    count = 0
    while new_i:
        count += 1
        sequence += i[-1]
        neighbours = neighbours_dict[i]

        if neighbours == []:
            all_sequences.append(sequence)
            sequence = ""
            new_i = []
            for key in neighbours_dict:
                if neighbours_dict[key]:
                    new_i.append(key)

            if new_i:
                i = np.random.choice(new_i)
                sequence += i[:k - 2]

            else:
                break

        else:
            x = np.random.choice(neighbours)
            for n in range(len(neighbours)):
                if neighbours[n] == x:
                    del neighbours[n]
                    break

            neighbours_dict[i] = neighbours
            i = x

    return all_sequences


def join_sequences(all_seq):
    """
    integrates loops into the main sequence
    :param all_seq: contains the main sequence and loop sequences to be integrated
    """

    while len(all_seq) > 1:

        for i in range(1, len(all_seq)):
            seq = all_seq[i]
            first = seq[:k - 2]
            last = seq[-1]

            new_seq = ""

            for j in range(len(all_seq[0]) - k + 1):
                string = all_seq[0]

                if string[j:j + k - 2] == first and string[j + k - 2] == last:
                    new_seq = string[:j] + seq + string[j + k - 1:]
                    break

            if new_seq != "":
                all_seq[0] = new_seq
                all_seq[i] = ""

            else:
                shuffled_loop = shuffle_loop(seq, all_seq[0], k)
                all_seq[i] = shuffled_loop[:]

        new = []
        for x in range(len(all_seq)):
            if all_seq[x] != "":
                new.append(all_seq[x])

        all_seq = new

    print(all_seq[0])


# main
filename = sys.argv[-1]

for i in range(len(sys.argv)):
    if sys.argv[i] == "-k":
        k = int(sys.argv[i+1])
    if sys.argv[i] == "-N":
        N = int(sys.argv[i + 1])


file = open(filename, 'r')
file = file.readline().strip()

klets = []
klet_sequence = []

for i in range(len(file)-k+2):
    new_klet = file[i:i+k-1]

    if new_klet not in klets:
        klets.append(new_klet)
    klet_sequence.append(new_klet)

# create dictionary with all neighbours for every klet
neighbours_dict = {}
for i in range(len(klet_sequence)-1):
    current_klet = str(klet_sequence[i])

    if current_klet in neighbours_dict.keys():
        x = neighbours_dict.get(current_klet)
        x.append(klet_sequence[i+1])

        neighbours_dict[current_klet] = x

    else:
        x = klet_sequence[i + 1]
        neighbours_dict[current_klet] = [x]

if klet_sequence[-1] not in neighbours_dict.keys():
    neighbours_dict[klet_sequence[-1]] = []


start = klet_sequence[0]
end = klet_sequence[-1]

count = 0
while count < N:

    #copy dictionary:
    d = {}
    for key in neighbours_dict:
        values = neighbours_dict[key]
        d[key] = values[:]

    all_sequences = shuffle(d, start)

    join_sequences(all_sequences)
    count += 1

