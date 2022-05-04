  
#AndaLatif 01046290
import random
import argparse
from pathlib import Path
import numpy as np
import copy



class KletGraph:
    def __init__(self,seq, k=2):
        self.seq = seq
        self.k = k
        self.nodes=[]
        self.klets = [seq[i:i+k] for i in range(len(seq) - k + 1)] 
        self.indeg, self.adj = self.build_multigraph()
        self.startnode = self.get_start_node()
               
        self.paths = []
         
    """public"""
       
    def solve(self, N):
        for i in range(N):
            self.find_random_euler_path()

    """private"""
    
    def build_multigraph(self):  
        #print(self.seq)   
        nodes=set()
        for klet in self.klets:
            nodes.add(klet[:-1])
            nodes.add(klet[1:])
        self.nodes=list(nodes)
        adj=  {k:[] for k in self.nodes}
        indeg = {k:0 for k in self.nodes}
        for klet in self.klets:
            n1 = klet[:-1]
            n2 =  klet[1:]
            adj[n1].append(n2)
            indeg[n2] += 1
        return indeg, adj
    
    def get_start_node(self):
        StartNode=[]
        for node in self.nodes:
            if self.indeg[node] - len(self.adj[node]) == -1:
                StartNode.append(node)
                
        if StartNode == []:
            StartNode = self.nodes
        return StartNode
        
    def find_random_euler_path(self):
        start_nodes = self.get_start_node()
        start_node = start_nodes[random.randint(0, len(start_nodes)) -1]
        self.copy_adj = copy.deepcopy(self.adj)
        self.current_path = [start_node]
        self.euler(start_node)
        self.solution()
        return

    def euler(self, node):
        while self.copy_adj[node] != []:
            next = self.copy_adj[node].pop(random.randint(0, len(self.copy_adj[node]) - 1))
            self.current_path.append(next)
            self.euler(next)
            
    def solution(self): 
        path = self.current_path[0]
        for i in range(1, len(self.current_path)):
            path +=  self.current_path[i][-1]
        self.paths.append(path)
        print(path)
         
def read_file(ifn):
    with open(ifn, "r") as input_file:
        return input_file.read().strip().upper()
def main():
    parser = argparse.ArgumentParser()  
    parser.add_argument("file", help="File to read input sequence from")
    parser.add_argument("-N", required=True, type=int, help="Number of sequences to generate")
    parser.add_argument("-k", required=True, type=int, help="which k-lets are to be considered, has to be greater or equal to 2")
    parser.add_argument("-s", default=None, type=int, required=False, help=" Seed, to make the results reproducible")
    argv=parser.parse_args()
    
    ifn = Path(argv.file)
    seq = read_file(ifn) 
    
    ofn = ifn.stem + ".out"      
    fout = open(ofn, "w")
    if argv.k<2:
        print("k must be at least 2")
    #random.seed(argv.s)
    
    graph = KletGraph(seq, argv.k)
    graph.solve(argv.N)
    for path in graph.paths:
        
        fout.write(path +"\n" )


if __name__ == "__main__":
    main()
   