import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument("file_name", help="a file to read")
parser.add_argument("-I", "--ignore", action="store_true", help="ignore case")
parser.add_argument("-l", "--list", action="store_true", help="print a list of counted words")
args = parser.parse_args()

word_count = 0
word_dict = {}

file_name = args.file_name

with open(file_name, "r") as r_file:
    for line in r_file:
        clean_line = re.sub('[^A-Za-z0-9]+', " ", line)
        words = clean_line.split()
        word_count += len(words)

        if args.ignore:
            for word in words:
                i_word = word.lower()
                if i_word not in word_dict:
                    word_dict[i_word] = 0
                word_dict[i_word] += 1
        else:
            for word in words:
                if word not in word_dict:
                    word_dict[word] = 0
                word_dict[word] += 1

if args.list:
    sorted_words_list = sorted(word_dict.items(), key=lambda x: x[1], reverse=True)

    for word_freq in sorted_words_list:
        print(f"{word_freq[0]}\t{word_freq[1]}")

else:
    print(f"{len(word_dict)} / {word_count}")
