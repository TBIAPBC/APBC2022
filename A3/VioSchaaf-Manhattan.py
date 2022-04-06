import sys
import numpy as np


def read_file(file):
    north_south = []
    west_east = []

    get_length = True
    for i in range(len(file)):
        if not file[i].startswith(('#', '\n')):
            if get_length:
                length = len(file[i])
                get_length = False

            if len(file[i]) == length:
                north_south.append(file[i].split())
            else:
                west_east.append(file[i].split())

    north_south = np.asarray(north_south).astype('float64')
    west_east = np.asarray(west_east).astype('float64')

    return north_south, west_east


def read_file_diag(file):
    north_south = []
    west_east = []
    diagonal = []

    get_length = True
    ns_row_count = 0
    we_row_count = 0
    for i in range(len(file)):
        if not file[i].startswith(('#', '\n')):
            if get_length:
                length = len(file[i])
                get_length = False

            if len(file[i]) == length:
                north_south.append(file[i].split())
                ns_row_count += 1
            elif we_row_count < ns_row_count + 1:
                west_east.append(file[i].split())
                we_row_count += 1
            else:
                diagonal.append(file[i].split())

    north_south = np.asarray(north_south).astype('float64')
    west_east = np.asarray(west_east).astype('float64')
    diagonal = np.asarray(diagonal).astype('float64')

    return north_south, west_east, diagonal


def HV(north_south, west_east):

    # initialize DP matrix and matrices to store information on which direction was chosen
    m = len(west_east)
    n = len(north_south[0])

    matrix = np.zeros((m, n))

    # initialize rows and columns of DP matrix
    for i in range(1, m):
        matrix[i, 0] = matrix[i - 1, 0] + north_south[i - 1, 0]

    for i in range(1, n):
        matrix[0, i] = matrix[0, i - 1] + west_east[0, i - 1]

    # calculate values for all possible paths and store the largest value in the matrix
    for i in range(1, m):
        for j in range(1, n):

            v1 = matrix[i - 1, j] + north_south[i - 1, j]
            v2 = matrix[i, j - 1] + west_east[i, j - 1]

            if v2 > v1:
                matrix[i, j] = v2

            else:
                matrix[i, j] = v1

    # obtain final result
    score = matrix[m - 1, n - 1]

    if score.is_integer():
        score = int(score)
    else:
        score = "{:.2f}".format(score)

    return score



def HV_path(north_south, west_east):

    # initialize DP matrix and matrices to store information on which direction was chosen
    m = len(west_east)
    n = len(north_south[0])

    matrix = np.zeros((m, n))
    north_south_path = np.zeros(north_south.shape)
    north_south_path[:, 0] = 1
    west_east_path = np.zeros(west_east.shape)
    west_east_path[0, :] = 1

    # initialize rows and columns of DP matrix

    for i in range(1, m):
        matrix[i, 0] = matrix[i - 1, 0] + north_south[i - 1, 0]

    for i in range(1, n):
        matrix[0, i] = matrix[0, i - 1] + west_east[0, i - 1]

    # calculate values for all possible paths and save the selected direction

    for i in range(1, m):
        for j in range(1, n):

            v1 = matrix[i - 1, j] + north_south[i - 1, j]
            v2 = matrix[i, j - 1] + west_east[i, j - 1]

            if v2 > v1:
                matrix[i, j] = v2
                west_east_path[i, j - 1] = 1

            else:
                matrix[i, j] = v1
                north_south_path[i - 1, j] = 1

    # obtain final result
    score = matrix[m - 1, n - 1]

    if score.is_integer():
        score = int(score)
    else:
        score = "{:.2f}".format(score)

    # trace back path
    string = ""

    row_nr = m - 1
    col_nr = n - 1

    while row_nr > 0 or col_nr > 0:
        if row_nr == 0 and col_nr > 0:
            string += "E"
            col_nr -= 1

        elif col_nr == 0 and row_nr > 0:
            string += "S"
            row_nr -= 1

        else:
            if north_south_path[row_nr - 1, col_nr] == 1:
                string += "S"
                row_nr -= 1
            else:
                string += "E"
                col_nr -= 1

    string_rev = ""
    for i in range(len(string) - 1, -1, -1):
        string_rev += string[i]

    return score, string_rev


def HVD(north_south, west_east, diagonal):

    # initialize DP matrix and matrices to store information on which direction was chosen
    m = len(west_east)
    n = len(north_south[0])
    matrix = np.zeros((m, n))

    # initialize rows and columns of DP matrix

    for i in range(1, m):
        matrix[i, 0] = matrix[i - 1, 0] + north_south[i - 1, 0]

    for i in range(1, n):
        matrix[0, i] = matrix[0, i - 1] + west_east[0, i - 1]

    # calculate values for all possible paths and store the largest value in the matrix

    for i in range(1, m):
        for j in range(1, n):

            v1 = matrix[i - 1, j] + north_south[i - 1, j]
            v2 = matrix[i, j - 1] + west_east[i, j - 1]
            v3 = matrix[i - 1, j - 1] + diagonal[i - 1, j - 1]

            max = np.amax([v1, v2, v3])

            if max == v1:
                matrix[i, j] = v1

            elif max == v2:
                matrix[i, j] = v2

            else:
                matrix[i, j] = v3

    # obtain final result
    score = matrix[m - 1, n - 1]

    if score.is_integer():
        score = int(score)
    else:
        score = "{:.2f}".format(score)

    return score


def HVD_path(north_south, west_east, diagonal):

    # initialize DP matrix and matrices to store information on which direction was chosen
    m = len(west_east)
    n = len(north_south[0])

    matrix = np.zeros((m, n))
    north_south_path = np.zeros(north_south.shape)
    north_south_path[:, 0] = 1
    west_east_path = np.zeros(west_east.shape)
    west_east_path[0, :] = 1
    diagonal_path = np.zeros(diagonal.shape)

    # initialize rows and columns of DP matrix
    for i in range(1, m):
        matrix[i, 0] = matrix[i - 1, 0] + north_south[i - 1, 0]

    for i in range(1, n):
        matrix[0, i] = matrix[0, i - 1] + west_east[0, i - 1]

    # calculate values for all possible paths and save the selected direction
    for i in range(1, m):
        for j in range(1, n):

            v1 = matrix[i - 1, j] + north_south[i - 1, j]
            v2 = matrix[i, j - 1] + west_east[i, j - 1]
            v3 = matrix[i - 1, j - 1] + diagonal[i - 1, j - 1]

            max = np.amax([v1, v2, v3])

            if max == v1:
                matrix[i, j] = v1
                north_south_path[i - 1, j] = 1

            elif max == v2:
                matrix[i, j] = v2
                west_east_path[i, j - 1] = 1

            else:
                matrix[i, j] = v3
                diagonal_path[i - 1, j - 1] = 1

    # obtain final result
    score = matrix[m - 1, n - 1]

    if score.is_integer():
        score = int(score)

    else:
        score = "{:.2f}".format(score)

    # trace back path
    string = ""

    row_nr = m - 1
    col_nr = n - 1

    while row_nr > 0 or col_nr > 0:
        if row_nr == 0 and col_nr > 0:
            string += "E"
            col_nr -= 1

        elif col_nr == 0 and row_nr > 0:
            string += "S"
            row_nr -= 1

        else:
            if north_south_path[row_nr - 1, col_nr] == 1:
                string += "S"
                row_nr -= 1
            elif west_east_path[row_nr, col_nr - 1] == 1:
                string += "E"
                col_nr -= 1
            else:
                string += "D"
                row_nr -= 1
                col_nr -= 1

    string_rev = ""
    for i in range(len(string) - 1, -1, -1):
        string_rev += string[i]

    return score, string_rev


def main():

    # load data and check for options
    filename = sys.argv[-1]

    file = open(filename, 'r')
    file = file.readlines()

    print_path = False
    diag = False

    if "-t" in sys.argv:
        print_path = True

    if "-d" in sys.argv:
        diag = True

    # obtain final result and print path if required
    if diag:
        north_south, west_east, diagonal = read_file_diag(file)

        if print_path:
            score, string = HVD_path(north_south, west_east, diagonal)
            print(score)
            print(string)

        else:
            score = HVD(north_south, west_east, diagonal)
            print(score)

    else:
        north_south, west_east = read_file(file)

        if print_path:
            score, string = HV_path(north_south, west_east)
            print(score)
            print(string)

        else:
            score = HV(north_south, west_east)
            print(score)


if __name__ == "__main__":
    main()






