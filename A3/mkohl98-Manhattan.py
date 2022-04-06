import argparse
from pathlib import Path
import sys


class Manhattan:
    def __init__(self, file, diagonal):
        self.file = file
        self.diagonal = diagonal

        self.n = 0
        self.m = 0
        self.arr_v = []
        self.arr_h = []
        self.arr_d = []

        self.matrix = []
        self.path = ""
        self.cost = 0

        self.solve()

    def read(self):
        first = True
        # counter to keeep track of length of matrix
        v_c, h_c = 0, 0
        # bool to know where to append
        append_h, append_v = False, True

        with open(self.file, "r") as input_file:
            for line in input_file:
                if line.startswith("\n") or line.startswith("#"):
                    pass

                else:
                    line.strip()
                    line_arr = line.replace("\n", "").split()
                    line_arr = [float(_) for _ in line_arr]

                    if first:
                        current_length = len(line_arr)
                        first = False

                    if append_v:
                        if len(line_arr) == current_length:
                            self.arr_v.append(line_arr)
                            v_c += 1
                        else:
                            self.arr_h.append(line_arr)
                            h_c += 1
                            append_v = False
                            append_h = True

                    elif append_h:
                        if h_c < v_c + 1:
                            self.arr_h.append(line_arr)
                            h_c += 1
                        else:
                            self.arr_d.append(line_arr)
                            append_h = False

                    else:
                        if self.diagonal:
                            self.arr_d.append(line_arr)

        self.n = len(self.arr_h[0]) + 1
        self.m = len(self.arr_v) + 1


    def fill(self):
        # init matrix
        self.matrix = [[0 for _ in range(self.n)] for __ in range(self.m)]

        # fill first row and line
        for i in range(1, self.n):
            self.matrix[0][i] = self.matrix[0][i - 1] + self.arr_h[0][i - 1]
        for i in range(1, self.m):
            self.matrix[i][0] = self.matrix[i - 1][0] + self.arr_v[i - 1][0]

        # fill matrix
        for i in range(1, self.m):
            for j in range(1, self.n):
                if self.diagonal:
                    self.matrix[i][j] = max(
                        # horizontal
                        self.matrix[i - 1][j] + self.arr_v[i - 1][j],
                        # vertical
                        self.matrix[i][j - 1] + self.arr_h[i][j - 1],
                        # diagonal
                        self.matrix[i - 1][j - 1] + self.arr_d[i - 1][j - 1]
                    )
                else:
                    self.matrix[i][j] = max(
                        # horizontal
                        self.matrix[i - 1][j] + self.arr_v[i - 1][j],
                        # vertical
                        self.matrix[i][j - 1] + self.arr_h[i][j - 1]
                    )

        self.cost = self.matrix[self.m - 1][self.n - 1]


    def trace_back(self):
        i, j = self.m - 1, self.n - 1
        while i > 0 and j > 0:
            if self.matrix[i][j] == self.matrix[i - 1][j] + self.arr_v[i - 1][j]:
                self.path += "S"
                i -= 1
            elif self.matrix[i][j] == self.matrix[i][j - 1] + self.arr_h[i][j - 1]:
                self.path += "E"
                j -= 1
            elif self.diagonal:
                self.path += "D"
                j -= 1
                i -= 1
            if i == 0 and j == 0:
                break
        while i > 0 and j == 0:
            self.path += "S"
            i -= 1
        while i == 0 and j > 0:
            self.path += "E"
            j -= 1

        self.path = self.path[::-1]


    def solve(self):
        self.read()
        self.fill()
        self.trace_back()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, help="Path to Input File")
    parser.add_argument("-d", "--diagonal", required=False, action="store_true", help="Enable diagonal pathing")
    parser.add_argument("-t", "--print_path", required=False, action="store_true", help="Print Path")
    args = parser.parse_args()

    path = Path(args.file)
    if not path.is_file():
        sys.tracebacklimit = 0
        raise FileNotFoundError(f'No file "{args.file}" found.')

    manhattan = Manhattan(args.file, args.diagonal)

    if manhattan.cost % int(manhattan.cost) == 0:
        print(int(manhattan.cost))
    else:
        print("{:.2f}".format(manhattan.cost))
    if args.print_path:
        print(manhattan.path)


if __name__ == "__main__":
    main()