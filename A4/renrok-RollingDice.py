import random
import sys


# calculated the frequencies of the nucleotides in the sequence
def calculateFrequency(sequence):
    frequencies = {'A': 0, 'G': 0, 'C': 0, 'U': 0}
    length = 0

    # count the nucleotides
    for seq in sequence:
        for nucleotide in seq:
            frequencies[nucleotide] += 1
        length += len(seq)

    # calculate frequency
    for nucleotide in frequencies:
        frequencies[nucleotide] = round(frequencies[nucleotide] / length, 3)

    # return only the frequencies in the order AGCU as list
    return list(frequencies.values())


# generates n random sequences with given frequencies and sequence
def generateRandomSequences(frequencies, sequence, n):
    randomSequences = []
    while n > 0:
        # random.choices returns a k sized list of elements chosen from the population by weights with replacement.
        currentSequence = random.choices(population=['A', 'G', 'C', 'U'],
                                         weights=frequencies,
                                         k=len(sequence))
        # join the generated list to a string
        randomSequences.append(''.join(currentSequence))
        n -= 1
    return randomSequences


def main():
    n = 0

    if "N" in sys.argv[1]:
        n = int(sys.argv[2])

    with open(sys.argv[3], 'r', encoding="utf-8") as reader:
        sequence = reader.read().strip()

    frequencies = calculateFrequency(sequence)
    randomSequences = generateRandomSequences(frequencies, sequence, n)

    # print(*frequencies)  #for testing purpose
    print(*randomSequences, sep='\n')
    # print(*calculateFrequency(randomSequences))  #for testing purpose


if __name__ == '__main__':
    main()
