import argparse
from pathlib import Path
import sys
import random
from copy import deepcopy


class Graph:
    def __init__(self, klets):
        # information from outside
        self.klets = klets
        self.k = len(klets[0])

        # graph representation
        self.nodes = []
        self.indegree = {}
        self.outdegree = {}
        self.adj = {}
        self.__build_graph()

        # working copies
        self.c_out = {}
        self.c_adj = {}

        self.current_path = []
        self.solutions = []

    """public methods"""
    def solve(self, n):
        # find n random euler paths
        for i in range(n):
            self.__random_euler()

        for solution in self.solutions:
            print(solution)

    """private methods"""
    def __build_graph(self):
        # create nodes and edges
        for klet in self.klets:
            # create nodes
            out_node = klet[1:]
            in_node = klet[:-1]
            if out_node not in self.nodes:
                self.nodes.append(out_node)
                self.outdegree[out_node] = 0
                self.indegree[out_node] = 0
                self.adj[out_node] = []
            if in_node not in self.nodes:
                self.nodes.append(in_node)
                self.outdegree[in_node] = 0
                self.indegree[in_node] = 0
                self.adj[in_node] = []

            # create edge
            self.outdegree[out_node] += 1
            self.indegree[in_node] += 1
            self.adj[out_node].append(in_node)

    def __get_start_node(self):
        for node in self.nodes:
            if self.indegree[node] - self.outdegree[node] == -1:
                return node
        return None

    def __random_euler(self):
        # main function to find euler path
        start_node = self.__get_start_node()
        if start_node is None:
            start_node = self.nodes[random.randint(0, len(self.nodes))]
        self.c_out = deepcopy(self.outdegree)
        self.c_adj = deepcopy(self.adj)
        self.current_path = []

        self.__euler_dfs(start_node)
        self.__path_to_seq()

    def __euler_dfs(self, node):
        # recursive dfs to find euler path
        while self.c_out[node] > 0:
            next_node = self.c_adj[node].pop(random.randint(0, len(self.c_adj[node]) - 1))
            self.c_out[node] -= 1

            self.__euler_dfs(next_node)

        self.current_path.append(node)

    def __path_to_seq(self):
        # transform euler path to sequence and return to solution
        self.current_path = self.current_path[::-1]
        path = self.current_path[0]
        for i in range(1, len(self.current_path)):
            path += self.current_path[i][-1]
        self.solutions.append(path)


def read_file(file):
    with open(file, "r") as input_file:
        return input_file.read().strip().upper()


def create_klets(seq, k):
    return [seq[i:i+k] for i in range(len(seq) - k + 1)]


def main():
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="File to read input sequence from")
    parser.add_argument("-k", "--k", default=3, type=int, required=False, help="k represents k-Let length")
    parser.add_argument("-N", "--n", default=1, type=int, required=False, help="Number of sequences to generate")
    parser.add_argument("-s", "--seed", default=None, type=int, required=False,
                        help="Seed for reconstruction of random processes")
    args = parser.parse_args()

    # validate arguments
    path = Path(args.input_file)
    if not path.is_file():
        sys.tracebacklimit = 0
        raise FileExistsError(f"File {args.input_file} does not exist!\n")
    if args.k < 2:
        sys.tracebacklimit = 0
        raise ValueError("k-Let length k must be greater or equal to 2!\n")
    if args.n < 1:
        sys.tracebacklimit = 0
        raise ValueError("N must be greater or equal to 1!\n")

    # execute code
    random.seed(args.seed)

    sequence = read_file(args.input_file)
    klets = create_klets(sequence, args.k)

    graph = Graph(klets)
    graph.solve(args.n)


if __name__ == "__main__":
    main()
