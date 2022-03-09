import argparse
import sys
import regex as re
#word_dictionary
def each_word(words):
    wcount = {}
    for w in words:
        if w not in wcount:
            wcount[w] = 1
        else:
            wcount[w] += 1
    return wcount

def Main():
    parser = argparse.ArgumentParser()
    # group = parser.add_mutually_exclusive_group()
    parser.add_argument("-l", "--list", help="words", action="store_true")
    parser.add_argument("-I", "--ignore", help="output file", action="store_true")
    parser.add_argument('filename', help="first input is filename")

    args = parser.parse_args()

    file = open(args.filename, 'r', encoding='utf-8')
    read_data = file.read()
    file.close()
    #all words in list
    words = re.sub(r'[^\w\s]', ' ', read_data)
    words = words.split()

    #sys.stdout = open('clemensheiderer-WordCount.out', 'wt')

    if args.ignore:
        lowercase_string = [str.lower() for str in words]
        words = lowercase_string


    word_dict = each_word(words)

    if args.list:
        dew_sorted = sorted(word_dict.items(), key=lambda kv: (-kv[1], kv[0]))

        for k, v in dew_sorted:
            print(f"{k} \t {v}")
    else:
        print(f"{len(word_dict)} / {len(words)}")


if __name__ == '__main__':
    Main()
