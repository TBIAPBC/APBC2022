#AndaLatif 01046290
from pathlib import Path
import argparse
from collections import Counter
import numpy as np

def read_file(ifn):
    try:
        f = open(ifn, 'r')
        for line in f :
            sequence=line.strip()
        f.close
        return sequence
    except FileNotFoundError:
            print("File not found " + ifn )
            
def calculate_freq(sequence):
    freq = Counter(sequence)
    for el in freq:
        freq[el] = freq[el]/len(sequence)       
    return freq

def random_seq(freq,seq_length, no_of_seq):
    result=[]
    for _ in range(no_of_seq):
        r = np.random.choice([b  for b  in freq], p=[pb for pb in freq.values()], size=seq_length)
        result.append("".join(e for e in r))
    return result    
    
    
if __name__ == "__main__":   
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type = str, help="Path of the input file.")
    parser.add_argument("-N", required=True, type=int, help="Number of sequences to be generated")
    argv=parser.parse_args()
    ifn = Path(argv.input_file)  
    ofn = ifn.stem+ ".out"      
    out = open(ofn, "w")
    sequence = read_file(argv.input_file)
    freq = calculate_freq(sequence) 
    #print(freq)
    result = random_seq(freq,len(sequence), argv.N )
    for seq in result:
        out.write(seq+"\n")
        print(seq)
    out.close()
   
    