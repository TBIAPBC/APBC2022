import argparse
import sys
import regex as re



def Main():
    parser = argparse.ArgumentParser()
    # group = parser.add_mutually_exclusive_group()
    parser.add_argument("-l", "--list", help="words", action="store_true")
    parser.add_argument("-I", "--ignore", help="output file", action="store_true")
    parser.add_argument('filename', help="first input is filename")

    args = parser.parse_args()

    file = open(args.filename, 'r', encoding='utf-8')
    read_data = file.read()
    new_string = re.sub(r'[^\w\s]', ' ', read_data)
    new_string = new_string.split()

    uppercase_string = [str for str in new_string if str[0].isupper()]
    lowercase_words = len(new_string) - len(uppercase_string)

    sys.stdout = open('clemensheiderer-WordCount.out', 'wt')

    if len(sys.argv) == 2:
        print(f"{lowercase_words} / {len(new_string)}")


    if args.ignore:
        lowercase_string = [str.lower() for str in new_string]
        new_string = lowercase_string


    if args.list:
        def each_word(words):
            wcount = {}
            for w in words:
                if w not in wcount:
                    wcount[w] = 1
                else:
                    wcount[w] += 1
            return wcount

        dew = each_word(new_string)


        dew_sorted = sorted(dew.items(), key=lambda kv: (-kv[1], kv[0]))


        for k, v in dew_sorted:
            print(f"{k} \t {v}")











if __name__ == '__main__':
    Main()