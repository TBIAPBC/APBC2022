import sys
import random



def weight(dice_line, split_letters):
    len_dice = len(split_letters)

    dice_p_G = dice_line.count('G') / len_dice
    dice_p_C = dice_line.count('C') / len_dice
    dice_p_A = dice_line.count('A') / len_dice
    dice_p_U = dice_line.count('U') / len_dice

    weights = [dice_p_G, dice_p_C, dice_p_A, dice_p_U]

    return weights, len_dice


def main():
    dice_line = ''
    with open(sys.argv[3], 'r') as f:
        for line in f:
            dice_line += line.rstrip()

    split_letters = [d for d in dice_line]

    weights, len_dice = weight(dice_line, split_letters)

    sys.argv[1] == "N"
    n = int(sys.argv[2])

    for _ in range(n):
        rolling_dices = ''.join(random.choices('GCAU', weights, k=len_dice))
        print(rolling_dices)



if __name__ == '__main__':
    main()







