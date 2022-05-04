#AndaLatif 01046290
import argparse
import numpy as np
import copy

class MonoShuffle:
    def __init__(self, ifn,N=0):
        self.ifn = ifn
        self.N = N
        self.seq=[]
        self.shuffled_seq=[]
        self.out = open(argv.input_file.split(".")[0] + ".out", 'w')

    def read_from_file(self,):    
        f = open(self.ifn, 'r')
        for line in f :
            self.seq = list(line.strip())
        print(self.seq)
        f.close
        return self.seq 

    def swap(self, i, j):
        aux = self.shuffled_seq[i]
        self.shuffled_seq[i]=self.shuffled_seq[j]
        self.shuffled_seq[j]=aux
        del aux

    def shuffle(self):
        for _ in range(0, self.N):
            indices=[]
            for i in range(len(self.seq)):
                indices.append(i)
                
            self.shuffled_seq=copy.deepcopy(self.seq)
            for i,_ in enumerate(self.shuffled_seq):
                self.swap(i=i, j=np.random.choice(indices))
                indices.pop(0)
            print("".join(self.shuffled_seq))

    
    
    
if __name__ == "__main__":   
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type = str, help="Path of the input file.")
    parser.add_argument("-N", required=True, type=int, help="Number of sequences to be generated")
    argv=parser.parse_args()
    RD = MonoShuffle(ifn=argv.input_file, N=argv.N)
    RD.read_from_file()
    RD.shuffle()
