import argparse
import re


def main():
    # setup parser
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str, help="Enter path of input file.")
    parser.add_argument("-i", "--ignore", required=False, action="store_true", help="Enable case-insensitivity mode.")
    parser.add_argument("-l", "--listing", required=False, action="store_true", help="Output word count listing.")
    parser.add_argument("-o", "--output_file", required=False, type=str, help="Enter optional output file name.")
    arg = parser.parse_args()

    # get input content
    with open(arg.input_file, "r", encoding="utf-8") as input_file:
        input_content = re.split("[^a-zA-Z0-9äöüß]", input_file.read())

    # count words
    words = {}
    word_num = 0
    for word in input_content:
        if word != "":
            word_num += 1
            if arg.ignore:
                word = word.lower()
            if word not in words:
                words[word] = 1
            else:
                words[word] += 1

    # output as listing
    if arg.listing:
        listing = ""
        for key, value in sorted(sorted(words.items(), key=lambda x: x[0]), reverse=True, key=lambda y: y[1]):
            listing += f"{key}\t{value}\n"

        if arg.output_file is None:
            print(listing)
        else:
            output_file = open(arg.output_file, "w", encoding="utf-8")
            output_file.write(listing)
            output_file.close()

    # output as simple word count
    else:
        if arg.output_file is None:
            print(f"{len(words)} / {word_num}\n")
        else:
            output_file = open(arg.output_file, "w", encoding="utf-8")
            output_file.write(f"{len(words)} / {word_num}\n")
            output_file.close()


if __name__ == '__main__':
    main()
