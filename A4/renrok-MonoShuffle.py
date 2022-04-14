import random
import sys


# shuffles the sequence by swapping item i with an item on a random positions j
def shuffleSequence(sequence, n):
    randomSequences = []
    length = len(sequence)
    while n > 0:
        currentSequence = sequence
        for i in range(length):
            # return a random int number n between [i, length-1]
            j = random.randint(i, length - 1)
            temp = currentSequence[i]
            currentSequence[i] = currentSequence[j]
            currentSequence[j] = temp
        randomSequences.append(''.join(map(str, currentSequence)))
        n -= 1
    return randomSequences


def main():
    n = 0

    if "N" in sys.argv[1]:
        n = int(sys.argv[2])

    with open(sys.argv[3], 'r', encoding="utf-8") as reader:
        sequence = reader.read().strip()

    randomSequences = shuffleSequence(list(sequence), n)

    print(*randomSequences, sep='\n')


if __name__ == '__main__':
    main()
