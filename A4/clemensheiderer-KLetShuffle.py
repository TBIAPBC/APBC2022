
from collections import defaultdict
import random
import argparse
parser = argparse.ArgumentParser()


parser.add_argument("-N", "--Number", nargs="?", const=1, type= int, required=True)
parser.add_argument("-k", "--kmer", nargs="?", const=1, type= int, required=True)



parser.add_argument('kletshufflefile')

args = parser.parse_args()
number = args.Number
kmer = args.kmer


class Graph_euler():
    def __init__(self, sequence, k):
        self.sequence = sequence
        self.k = k
        self.kmers_path = []
        self.node = set()


    def nodes(self):

        for i in range(len(self.sequence) - self.k + 1):
            self.kmers_path.append((self.sequence[i:i + self.k - 1], self.sequence[i + 1:i + self.k]))
            self.node.add(self.sequence[i:i + self.k - 1])
            self.node.add(self.sequence[i + 1:i + self.k])
        return self.kmers_path

    def kmers_outwards(self):
        self.kmers_path = self.nodes()

        dict_outer_edges = defaultdict(list)
        for i, j in self.kmers_path:
            dict_outer_edges[i].append(j)
        edges = dict(dict_outer_edges)

        return edges


    def euler_walk_k_shuffle(self):
        self.edges = self.kmers_outwards()
        start_kmer = list(self.edges.keys())[0]
        stack = [start_kmer]
        path = []

        while len(stack) > 0:
            node = stack[-1]
            if node not in self.edges or len(self.edges[node]) == 0:
                path.append(node)

                stack.pop()
            else:
                index = random.randint(0, len(self.edges[node]) - 1)

                stack.append(self.edges[node][index])
                self.edges[node].pop(index)

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
            class_graph = Graph_euler(sequence, k)
            euler_path_kmers = class_graph.euler_walk_k_shuffle()


            klet_shuffled = "".join(kmer[0] for kmer in euler_path_kmers[0:len(euler_path_kmers) - 1]) + \
                            euler_path_kmers[-1]
            print(klet_shuffled)




if __name__ == '__main__':
    main()










