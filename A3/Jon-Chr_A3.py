import os
import sys
import numpy as np

# Command Line Arguments
diagonal = False
best_path = False

for cmd in sys.argv:
    if cmd.lower() == "-t":
        best_path = True
    elif cmd.lower() == "-d":
        diagonal = True
    else:
        file = cmd


def file_to_matrix(file):
    # Open File and create a list -> matrix
    A = []
    f = open(file)
    for line in f:
        if line[0] == "#":
            continue
        else:
            line = line.strip().split()
            if len(line) > 0:
                row = [float(x) for x in line]
                A.append(row)
    f.close()
    return A


def backtracing(C, down, right, dia, n, m, diag=False):
    path = ""
    if diag:
        res = float(C[n][m])

        while C[n][m] > 0:
            if round(float(C[n][m] - C[n - 1][m]), 2) == float(down[n - 1][m]) or C[n][m] == C[n][0]:
                path += "S"
                n -= 1
            elif round(float(C[n][m] - C[n][m - 1]), 2) == float(right[n][m - 1]) or C[n][m] == C[0][m]:
                path += "E"
                m -= 1
            elif round(float(C[n][m] - C[n - 1][m - 1]), 2) == float(dia[n - 1][m - 1]):
                path += "D"
                n -= 1
                m -= 1

    else:
        res = int(C[n][m])

        while C[n][m] > 0:
            if float(C[n][m] - C[n - 1][m]) == float(down[n - 1][m]):
                path += "S"
                n -= 1
            elif float(C[n][m] - C[n][m - 1]) == float(right[n][m - 1]):
                path += "E"
                m -= 1

    path = path[::-1]  # Reverse Order

    return res, path


def solve_manhatten(A, diagonal):
    # Solve Manhatten Problem
    # Take care of diagonal Case
    if diagonal:

        d = len(A[0])

        A_down = A[:d - 1]
        A_right = A[d - 1:2 * d - 1]
        A_diag = A[2 * d - 1:]

        # print(A_down, "\n\n", A_right, "\n\n", A_diag)
        C = np.zeros((d, d))

        for i in range(1, d):
            C[i][0] = C[i - 1][0] + float(A_down[i - 1][0])
        for j in range(1, d):
            C[0][j] = float(C[0][j - 1]) + float(A_right[0][j - 1])
        for i in range(1, d):
            for j in range(1, d):
                C[i][j] = max(float(C[i - 1][j]) + float(A_down[i - 1][j]), float(C[i][j - 1]) + float(A_right[i][j - 1]),
                              + float(C[i - 1][j - 1]) + float(A_diag[i - 1][j - 1]))

        d -= 1

        res, path = backtracing(C, A_down, A_right, A_diag, d, d, diag=True)

    else:
        # Separate Matrix into down and right matrix (not diagonal)

        n = len(A[0])
        m = int((len(A) + 1) / 2)

        cut = 0
        for i in A:
            if len(i) == n:
                cut += 1
            else:
                break

        A_down = A[:cut]
        A_right = A[cut:]

        C = np.zeros((n, m))

        for i in range(1, n - 1):
            C[i][0] = C[i - 1][0] + float(A_down[i - 1][0])
        for j in range(1, m - 1):
            C[0][j] = float(C[0][j - 1]) + float(A_right[0][j - 1])
        for i in range(1, n):
            for j in range(1, m):
                C[i][j] = max(float(C[i - 1][j]) + float(A_down[i - 1][j]),
                              float(C[i][j - 1]) + float(A_right[i][j - 1]))

        n -= 1
        m -= 1
        A_diag = 0

        res, path = backtracing(C, A_down, A_right, A_diag, n, m, diag=False)

    return res, path


# Main
A = file_to_matrix(file)
res, path = solve_manhatten(A, diagonal)
if best_path:
    print(round(res, 2), "\n" + path)
else:
    print(round(res, 2))

