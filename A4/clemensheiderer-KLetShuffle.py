
import random
from collections import defaultdict
import argparse
parser = argparse.ArgumentParser()


parser.add_argument("-N", "--Number", nargs="?", const=1, type= int, required=True)
parser.add_argument("-k", "--kmer", nargs="?", const=1, type= int, required=True)



parser.add_argument('kletshufflefile')

args = parser.parse_args()
number = args.Number
kmer = args.kmer

def graph(sequence, k):
    kmers_path = []
    node = set()

    for i in range(len(sequence) - k + 1):
        kmers_path.append((sequence[i:i+k-1], sequence[i+1:i+k]))
        node.add(sequence[i:i+k-1])
        node.add(sequence[i+1:i+k])
    return kmers_path, node


def kmers_outwards(kmers_path):
    dict_outer_edges = defaultdict(list)
    for i, j in kmers_path:
        dict_outer_edges[i].append(j)
    return dict_outer_edges


def euler_walk_k_shuffle(start_kmer, edges):

    stack = [start_kmer]
    path = []

    while len(stack) > 0:
        node = stack[-1]
        if node not in edges or len(edges[node]) == 0:
            path.append(node)

            stack.pop()
        else:
            index = random.randint(0, len(edges[node]) - 1)

            stack.append(edges[node][index])
            edges[node].pop(index)

    path.reverse()

    return path


def main():
    def get_sequence(file):
        with open(file, "r") as input:
            seq = input.readline().strip()
        return seq

    sequence = get_sequence(args.kletshufflefile)



    if args.Number:

        for i in range(number):
            args.kmer
            k = kmer

            kmers_path, nodes = graph(sequence, k)

            dict_outer_edges = kmers_outwards(kmers_path)

            edges = dict(dict_outer_edges)

            start_kmer = list(edges.keys())[0]



            euler_path_kmers = euler_walk_k_shuffle(start_kmer, edges)

            klet_shuffled = "".join(kmer[0] for kmer in euler_path_kmers[0:len(euler_path_kmers) - 1]) + euler_path_kmers[-1]
            print(klet_shuffled)


if __name__ == '__main__':
    main()












