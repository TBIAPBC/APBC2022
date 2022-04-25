#carolina atria
#11835854
#Rolling Dice
import random
import sys

def generate_random(length,weights):
    no_of_seq = int(sys.argv[2])
    nucleotides = "ACGU"
    list_of_random=[]
    i=0
    while i < no_of_seq:
        random_seq =(random.choices(nucleotides,weights,k=length))
        list_of_random.append("".join(random_seq))
        i+=1
    print("\n".join(list_of_random))

def calculate_frequencies(string):
    weights=[]
    nucleotide_freq={"A":0,"C":0,"G":0,"U":0}
    for i in string:
        nucleotide_freq[i] += 1
    for values in nucleotide_freq:
        nucleotide_freq[values] = (nucleotide_freq[values])/len(string)
        weights.append(nucleotide_freq[values])
    # print(weights) #to see the frequencies
    generate_random(len(string),weights)

def string_reader():
    filename = sys.argv[3]
    with open(filename) as f:
        content = f.read().strip("\n")
        calculate_frequencies(content)

string_reader()