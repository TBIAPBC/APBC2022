import sys
import random


def weight(dice_line):
    len_dice = len(dice_line)

    dice_p_G = dice_line.count('G') / len_dice
    dice_p_C = dice_line.count('C') / len_dice
    dice_p_A = dice_line.count('A') / len_dice
    dice_p_U = dice_line.count('U') / len_dice

    weights = [dice_p_G, dice_p_C, dice_p_A, dice_p_U]

    return weights, len_dice


def main():
    if len(sys.argv) < 4:
        print("it needs flag -N with following int number as input\n")
        print("Usage: %s -N [integer] rolling_dice_number.in" % sys.argv[0])
        sys.exit(1)



    dice_line = ''
    with open(sys.argv[3], 'r') as f:
        for line in f:
            dice_line += line.rstrip()


    weights, len_dice = weight(dice_line)


    if sys.argv[1] == "-N":
        n = int(sys.argv[2])
        for _ in range(n):
            rolling_dices = ''.join(random.choices('GCAU', weights, k=len_dice))
            print(rolling_dices)


if __name__ == '__main__':
    main()










