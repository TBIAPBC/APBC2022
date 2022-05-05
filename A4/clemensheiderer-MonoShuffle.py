import random

import argparse
parser = argparse.ArgumentParser()



parser.add_argument("-N", "--Number", nargs="?", const=1, type= int, required=True)

parser.add_argument('monoshufflefile')

args = parser.parse_args()
number = args.Number



def mono_shuffle(shuffled):
    for i in range(0, len(shuffled) - 1, +1):
        choose_index = random.randint(i, len(shuffled) - 1)
        shuffled[choose_index], shuffled[i] = shuffled[i], shuffled[choose_index]

    return shuffled


def main():
    dice_line = ''
    with open(args.monoshufflefile, 'r') as f:
        for line in f:
            dice_line += line.rstrip()


    if args.Number:
        for i in range(number):
            mono_shuffled_list = mono_shuffle(list(dice_line))
            mono_shuffle_string = "".join(mono_shuffled_list)

            print(mono_shuffle_string)

if __name__ == '__main__':
    main()
