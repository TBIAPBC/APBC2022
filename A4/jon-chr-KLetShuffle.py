import pdb
import sys
import random
import numpy as np
from copy import deepcopy


class Graph():

    def __init__(self, seq, k):
        self.node_bases = self.get_nodes_bases(seq, k)
        self.edges = self.get_edges(seq, k)
        self.edge_idxs = self.edge_to_idx()
        self.adjecent_edges = self.get_adjecency()

    def get_nodes_bases(self, seq, k):
        k_lets = []
        length = len(seq)
        for i in range(length - k):
            # k-let till length -1
            k_let = seq[i:i + k - 1]
            k_lets.append(k_let)

        node_dict = {}
        for key in seq:
            if key in node_dict:
                continue
            else:
                node_dict[key] = None

        node_bases = list(node_dict.keys())
        return node_bases

    def get_edges(self, seq, k):
        edges = []
        length = len(seq)
        for i in range(length - k + 1):
            edge = [seq[i:i + k - 1], seq[i + 1:i + k]]
            edges.append(edge)
        return edges

    # Turn edges into ids corresponding to index of unique bases
    def edge_to_idx(self):
        edge_idx = []
        edges = self.edges
        nodes = self.node_bases
        for edge in edges:
            idxs = []
            idxs.append(nodes.index(edge[0]))
            idxs.append(nodes.index(edge[1]))
            edge_idx.append(idxs)
        return edge_idx

    def get_adjecency(self):
        edge_idx = self.edge_idxs
        adjecency = {}
        for edge_id in edge_idx:
            edge = edge_id[0]
            ne_edge = edge_id[1]
            if edge in adjecency.keys():
                temp = adjecency[edge]
                temp.append(ne_edge)
                adjecency[edge] = temp
            else:
                adjecency[edge] = [ne_edge]
        return adjecency


class EulerPath():

    def __init__(self, edges, adj, length):
        self.indeg = self.degree(edges, length, "in")
        self.outdeg = self.degree(edges, length, "out")
        self.valid_path = self.is_valid_path()
        self.start_node = 0
        self.paths = []

    def degree(self, edges, n, direction):
        ind = 1 if direction == "in" else 0
        degree = []
        for c in range(n):
            i = 0
            for edge in edges:
                if edge[ind] == c:
                    i += 1
            degree.append(i)

        return degree

    def is_valid_path(self):
        start_node = 0
        start = 0
        end = 0
        indeg = self.indeg
        outdeg = self.outdeg
        safety = True
        for i in range(len(outdeg)):
            io = indeg[i] - outdeg[i]
            oi = outdeg[i] - indeg[i]

            if io == 1:
                end += 1
            elif oi == 1:
                start += 1
                start_node = i
            elif io > 1 or oi > 1:
                safety = False

            if safety == False:
                self.start_node = start_node
                return False
            else:
                if (start == 0 and end == 0) or (start == 1 and end == 1):
                    self.start_node = start_node
                    return True

    def set_start(self):
        outdeg = np.array(self.outdeg)
        if self.start_node == 0:
            sn = np.where(outdeg > 0)[0]
            i = random.randint(0, len(sn) - 1)
            self.start_node = sn[i]

    def depth_first_search(self, start, adj, outdeg):
        paths = self.paths
        while outdeg[start] != 0:
            rnd_ind = random.randint(0, len(adj[start]) - 1)
            next_pos = adj[start].pop(rnd_ind)
            outdeg[start] -= 1
            paths.append(start)
            self.depth_first_search(next_pos, adj, outdeg)

        self.paths = paths


# Main
N = 30
k = 2
file = "KLetShuffle-test30_k2.in"

# Get Sys ArgV
counter = 0
for cmd in sys.argv:
    counter += 1
    if cmd.lower() == "-n" or cmd.lower() == "n":
        N = int(sys.argv[counter])
    elif cmd.lower() == "-k" or cmd.lower() == "k":
        k = int(sys.argv[counter])
    elif cmd[-2:] == "in":
        file = cmd


f = open(file)
seq = ""
for line in f:
    seq += line.strip()
f.close()

g = Graph(seq, k)
our_paths = []

for i in range(1000):
    edge_ids = g.edge_idxs
    adj_dict = deepcopy(g.adjecent_edges)

    path = EulerPath(edge_ids, adj_dict, N)

    if path.valid_path:
        # path.set_start()
        start_node = path.start_node
        outdeg = path.outdeg
        path.depth_first_search(start_node, adj_dict, outdeg)

        if len(path.paths) == len(edge_ids):
            pos_path = path.paths[::-1]

            if pos_path not in our_paths:
                our_paths.append(pos_path)

nb = g.node_bases
for i in range(N):
    res = random.choice(our_paths)
    solution = []
    for j in range(len(res)):
        solution.append(nb[res[j]][-1])
    print("".join(solution))

