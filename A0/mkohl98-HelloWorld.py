import argparse


def main():
    # setup parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_file", required=True, type=str, help="Enter Path of input file.")
    parser.add_argument("-o", "--output_file", type=str, required=False, help="Enter optional name for output file")
    a = parser.parse_args()

    # read input file
    with open(a.input_file, "r") as input_file:
        input_content = input_file.read()

    # give optional output file
    if a.output_file is not None:
        output_file = open(a.output_file, "w")
        output_file.write("Hello World!\n" + input_content)
        output_file.close()

    # default output
    print("Hello World!\n" + input_content)


if __name__ == "__main__":
    main()
