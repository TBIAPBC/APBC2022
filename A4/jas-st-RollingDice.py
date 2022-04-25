import random
import sys

def input_verifier():
    if len(sys.argv) != 4:
        print("Please provide the correct arguments! \n  file.py -N [int] input_file.%txt")
   ## make sure that the file name is in the last position  
    elif len(sys.argv)>2 and (sys.argv[-1].isdigit() or (sys.argv[-1] == "-N")):
        print("Please provide the correct arguments! \n  file.py -N [int] input_file.%txt")
    else:
        return True

def get_sequence(file):
    with open(file,"r") as input:
        seq = input.readline().strip()
    return seq

def get_frequences(seq):
    freq = {}

    for char in seq:
        if char not in freq:
            freq[char] = 1
        else:
            freq[char] += 1

    prob = 0
    for base in freq.keys():         #calculate cumulative frequences
       prob += freq[base]/len(seq)
       freq[base] = prob
    
    return freq

def generate_seq(freq, n):
    seq = ""
    keys = list(freq.keys())
    for i in range(n):
        k = random.random()                  ### generates a random float between 0 and 1
                                           
        for i in range(len(keys)):          ### then checks in what range is that number
            if k < freq[keys[i]]:           ### and adds the corresponding base
                seq += keys[i]
                break
    return seq
        



if __name__ == "__main__":

    if input_verifier():

        ### input
        arguments = sys.argv
        file_name = arguments[-1]
        N = int(arguments[arguments.index("-N")+1])

        sequence = get_sequence(file_name)
        frequences = get_frequences(sequence)

        for i in range(N):
            print(generate_seq(frequences,len(sequence)))



        

               