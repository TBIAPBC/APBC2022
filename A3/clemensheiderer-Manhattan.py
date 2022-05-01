import numpy as np
import argparse

parser = argparse.ArgumentParser(description='Manhattan',
                                 usage="""


                                 use "%(prog)s --help" for more information


                                     """,
                                 formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument('inputfile')

parser.add_argument("-t", "--t_path", help="""
    load it with:filename.py -t Manhattan-testHV1.in

    best path
                      """, action="store_true")

parser.add_argument("-d", "--diagonal", help="""
    load it with:filename.py -d Manhattan-testHVD1.in

    inlcludes diagonal path
                      """, action="store_true")

args = parser.parse_args()


if not args.diagonal:
    with open(args.inputfile) as f:
        list = []
        for line in f:
            li = line.strip()
            if not li.startswith("#"):
                b = line.split()
                result = (np.array(b, dtype=float)).round(decimals=2)
                if len(result) != 0:
                    list.append(result)



    def initializing_matrix(list):
        east = []
        south = []
        for i in range(len(list)):
            if len(list[i]) == len(list[0]):
                south.append(list[i])
            else:
                east.append(list[i])
        east = np.array(east)
        south = np.array(south)
        y = len(east[0]) + 1
        x = len(south) + 1
        a = len(east[0]) + 1

        matrix = np.zeros((x, y))
        matrix[0, 0] = 0

        matrix_backtrack = np.zeros((x, y))

        matrix[0, 0] = 0
        return matrix, matrix_backtrack, x, y, east, south


    matrix, matrix_backtrack, x, y, east, south = initializing_matrix(list)


    def matrix_calculation(matrix, matrix_backtrack, x, y, east, south):
        up, left = 1, -1

        for col in range(1, y):
            matrix[0, col] = matrix[0, col - 1] + east[0, col - 1]
            matrix_backtrack[0, col] = left

        for row in range(1, x):
            matrix[row, 0] = matrix[row - 1, 0] + south[row - 1, 0]
            matrix_backtrack[row, 0] = up

        for row in range(1, x):
            for col in range(1, y):
                matrix[row, col] = max(matrix[row - 1, col] + south[row - 1, col], matrix[row, col - 1] + east[row, col - 1])
                if matrix[row, col - 1] + east[row, col - 1] > matrix[row - 1, col] + south[row - 1, col]:matrix_backtrack[row, col] = left

                else:
                    matrix_backtrack[row, col] = up

        return matrix, matrix_backtrack


    matrix, matrix_backtrack = matrix_calculation(matrix, matrix_backtrack, x, y, east, south)
    m = matrix[-1][-1]
    m_2_dec = "{:.2f}".format(matrix[-1][-1])

    is_it_int = str(float(m_2_dec) - int(float(m_2_dec)))[1:]
    if is_it_int == ".0":
        print(round(float(m_2_dec)))
    else:
        print(m_2_dec)


    if args.t_path:

        def backtrack_path(matrix_backtrack, x, y):
            up, left = 1, -1
            path_backtrack = ""
            row = x - 1
            col = y - 1
            while row > 0 or col > 0:
                if matrix_backtrack[row, col] == up:
                    path_backtrack = "S" + path_backtrack
                    row = row - 1
                else:
                    path_backtrack = "E" + path_backtrack
                    col = col - 1
            return path_backtrack


        path_backtrack = backtrack_path(matrix_backtrack, x, y)
        print(path_backtrack)


if args.diagonal:
    fasta_seq_list = [f.strip() for f in open(args.inputfile).readlines()]
    multiple_fasta_dict = {}
    for line in fasta_seq_list:
        dom = []
        if not line:
            continue
        if line[0] == '#':
            reads = line
            if reads not in multiple_fasta_dict:
                multiple_fasta_dict[line] = []
            continue
        line = line.split()
        def trunc(values, decs=0):
            return np.trunc(values * 10 ** decs) / (10 ** decs)

        result = np.array(line, dtype=float)
        result = trunc(result, decs = 2)
        dom.append(result)
        multiple_fasta_dict[reads] += dom

    n = []
    for k, v in multiple_fasta_dict.items():
        if len(v) >= 1:
            n.append(np.array(v))

    south = n[0]
    east = n[1]
    diag = n[2]
    y = len(east[0]) + 1
    x = len(south) + 1
    a = len(east[0]) + 1
    matrix = np.zeros((x, y))
    matrix[0, 0] = 0
    matrix_backtrack = np.zeros((x, y))


    def matrix_calculation_d(matrix, matrix_backtrack, x, y, east, south):
        up = 1
        left = -1
        dig = 2
        for col in range(1, y):
            matrix[0, col] = matrix[0, col - 1] + east[0, col - 1]
            matrix_backtrack[0, col] = left

        for row in range(1, x):
            matrix[row, 0] = matrix[row - 1, 0] + south[row - 1, 0]
            matrix_backtrack[row, 0] = up

        for row in range(1, x):
            for col in range(1, y):
                matrix[row, col] = max(matrix[row - 1, col] + south[row - 1, col], matrix[row, col - 1] + east[row, col - 1], matrix[row - 1, col - 1] + diag[row - 1, col - 1])

                if matrix[row - 1, col] + south[row - 1, col] > matrix[row, col - 1] + east[row, col - 1] and \
                        matrix[row - 1, col] + south[row - 1, col] > matrix[row - 1, col - 1] + diag[row - 1, col - 1]:matrix_backtrack[row, col] = up
                if matrix[row - 1, col - 1] + diag[row - 1, col - 1] > matrix[row - 1, col] + south[row - 1, col] and \
                        matrix[row - 1, col - 1] + diag[row - 1, col - 1] > matrix[row, col - 1] + east[row, col - 1]:matrix_backtrack[row, col] = dig
                if matrix[row, col - 1] + east[row, col - 1] > matrix[row - 1, col] + south[row - 1, col] and \
                        matrix[row, col - 1] + east[row, col - 1] > matrix[row - 1, col - 1] + diag[row - 1, col - 1]:matrix_backtrack[row, col] = left

        return matrix, matrix_backtrack


    matrix, matrix_backtrack = matrix_calculation_d(matrix, matrix_backtrack, x, y, east, south)


    m_2_dec = "{:.2f}".format(matrix[-1][-1])
    is_it_int = str(float(m_2_dec) - int(float(m_2_dec)))[1:]

    if is_it_int == ".0":
        print(round(float(m_2_dec)))
    else:
        print(m_2_dec)


    if args.t_path:
        def backtrack_path_d(matrix_backtrack, x, y):
            up = 1
            left = -1
            dig = 2
            path_backtrack = ""
            row = x - 1
            col = y - 1
            while row > 0 or col > 0:
                if matrix_backtrack[row, col] == up:
                    path_backtrack = "S" + path_backtrack
                    row = row - 1
                if matrix_backtrack[row, col] == dig:
                    path_backtrack = "D" + path_backtrack
                    row = row - 1
                    col = col - 1
                if matrix_backtrack[row, col] == left:
                    path_backtrack = "E" + path_backtrack
                    col = col - 1
            return path_backtrack

        path_backtrack = backtrack_path_d(matrix_backtrack, x, y)

        print(path_backtrack)




