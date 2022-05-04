#AndaLatif 01046290
from multiprocessing.dummy import Array
import random
import argparse
from pathlib import Path
import pandas as pd
import numpy as np
import copy


class KletGraph:
    def __init__(self,seq, k):
        self.seq = seq
        self.k = k
        self.nodes=[]
        self.klets = [seq[i:i+k] for i in range(len(seq) - k + 1)] 
         #data frame: node, nbhd, seen next
        self.indeg, self.adj, self.df = self.build_multigraph()
        self.startnode = []
        self.pathsdf = [] 
        self.current_pathdf=[]
        self.dfcopy= pd.DataFrame.from_dict({node:[self.adj[node], 0, ""] for node in self.nodes}, orient='index', columns=['nbhd', 'seen', 'next'])
    """public"""
       
    def solve(self, N=1):
         for i in range(N):
            self.dfcopy=copy.deepcopy(self.df)
            self.result()
   
    """private"""
    
    def build_multigraph(self): 
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
        df = pd.DataFrame.from_dict({node:[adj[node], 0, ""] for node in nodes}, orient='index', columns=['nbhd', 'seen', 'next'])
        return indeg, adj, df
    
    def findSpanningTree(self):
        start = self.seq[:self.k-1]
        self.dfcopy.loc[start  , 'seen'] = 1
        end = self.seq[len(self.seq)-self.k+1: ]
        self.dfcopy.loc[end, 'seen'] = 1
        self.dfcopy.loc[end, 'next'] =  None
        current = start
        #self.dfcopy.loc[current  , 'seen'] = 1
        while not (self.dfcopy['seen'] == 1).all():
                self.dfcopy.loc[current  , 'seen'] = 1
                if len(self.dfcopy.loc[current  , 'nbhd'])>0:
                    index = random.randint(0, len(self.dfcopy.loc[current  , 'nbhd'])-1)
                    next = self.dfcopy.loc[current  , 'nbhd'][index]                    
                    self.dfcopy.loc[current  , 'next'] = next
                    currnbhd= self.dfcopy.loc[current  , 'nbhd']                    
                    currnbhd.pop(currnbhd.index(next))                    
                    currnbhd = shuffle(currnbhd)
                    currnbhd.append(next)
                    self.dfcopy.loc[current  , 'nbhd'].clear()
                    for el in currnbhd: 
                        self.dfcopy.loc[current  , 'nbhd'].append(el)         
                
                    current = next
                    if self.dfcopy.loc[next  , 'seen'] == 1:
                        #pick a random unseen
                        unseen = copy.deepcopy(self.dfcopy[self.dfcopy.seen.eq(0)])
                        unseen = unseen.index.to_numpy()
                        if len(unseen)>0:
                            current= unseen[random.randint(0, len(unseen)-1)]
                        else:
                            return
                    else:
                        current = next
                    
                    
             
        return 
        
    def get_start_node(self): ## can be deleted
        StartNode=[]
        for node in self.nodes:
            if self.indeg[node] - len(self.adj[node]) == -1:
                ##actually the first k-1 let of the sequence will always satisfy this , so this is actually not needed for the latest version
                StartNode.append(node)
        if StartNode == []:
            StartNode = self.nodes
        return StartNode
    
    def result(self):
        # self.dfcopy=copy.deepcopy(self.df)
        self.findSpanningTree()
        #print(self.dfcopy)
        start_nodes = self.get_start_node()
        start_node = start_nodes[random.randint(0, len(start_nodes)) -1]  
        self.current_pathdf.clear() 
        self.current_pathdf.append(start_node)
        self.eulerdf(start_node)
        self.solution()
        
        return
        
    def eulerdf(self, current):
        while not (self.dfcopy.loc[current  , 'nbhd'] == []):
            next = self.dfcopy.loc[current  , 'nbhd'][0]
            self.dfcopy.loc[current,'nbhd'].pop(0)
            self.current_pathdf.append(next)
            self.eulerdf(next)

    def solution(self): 
        path = self.current_pathdf[0]
        for i in range(1, len(self.current_pathdf)):
            path +=  self.current_pathdf[i][-1]
        self.pathsdf.append(path)
        #print(path)
 
def shuffle(listseq):
    
    if len(listseq)>1:
        for i in range(0, len(listseq)-1):
            j = random.randrange(i, len(listseq)-1)
            aux = listseq[i]
            listseq[i] = listseq[j]
            listseq[j] = aux
    return list(listseq)

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
  
       
    for _ in range(argv.N):
        graph = KletGraph(seq, argv.k) 
        graph.solve()
        for path in graph.pathsdf:
                fout.write(path +"\n" )
                print(path)
        
        


if __name__ == "__main__":
    main()
 