import argparse


def main():
    # setup parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_file", required=True, type=str, help="Enter Path of input file")
    parser.add_argument("-o", "--output_file", type=str, required=False, help="Enter optional file name for output file")
    a = parser.parse_args()

    # read and create files
    input_file = open(a.input_file, "r")
    if a.output_file is not None:
        output_file = open(a.output_file, "w")
    else:
        output_file = open("HelloWorld-test1.out", "w")

    # write in file
    output_file.write("Hello World!\n")
    for line in input_file:
        output_file.write(line)

    # close files
    input_file.close(), output_file.close()


if __name__ == "__main__":
    main()
