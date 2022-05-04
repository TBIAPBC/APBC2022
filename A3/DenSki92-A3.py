import argparse


def reverse(string):
    '''
    takes a string and outputs it in reverse
    '''
    if len(string) == 0:
        return string
    else:
        return reverse(string[1:]) + string[0]



parser = argparse.ArgumentParser()
parser.add_argument("file_name", help="a file to read")
parser.add_argument("-t", "--printpath", action="store_true", help="prints out the best path")
args = parser.parse_args()

file_name = args.file_name

# create directional lists(ns, we, dia), read file, write data into the lists
ns = []
we = []
dia = []
first_line = True

with open(file_name, "r") as df:
    i = 0
    for line in df:
        if not line.startswith("#") and not line.startswith("\n"):

            line = [float(value) for value in line.strip().split()]
            if first_line:
                start_l = len(line)
                first_line = False
            if len(line) == start_l:
                ns.append(line)
            elif i <= len(line):
                we.append(line)
                i += 1
            else:
                dia.append(line)


ns_len = len(ns)
we_len = len(we[0])

# if dia remains empty, fill it with zeros
if not dia:
    dia = [[0 for m in range(we_len)] for n in range(ns_len)]


# Implement a 2D DP matrix that stores the optimal path weight from the start to each crossing (or corner)

matrix = [[0 for m in range(we_len+1)] for n in range(ns_len+1)]
for n in range(1, ns_len+1):
    matrix[n][0] = matrix[n-1][0] + ns[n-1][0]
for m in range(1, we_len+1):
    matrix[0][m] = matrix[0][m-1] + we[0][m-1]
for n in range(1, ns_len+1):
    for m in range(1, we_len+1):
        matrix[n][m] = max(matrix[n-1][m] + ns[n-1][m], matrix[n][m-1] + we[n][m-1], matrix[n-1][m-1] + dia[n-1][m-1])


# The final result is computed at the end corner
max_value = matrix[ns_len][we_len]



print(int(max_value))


# The solution is obtained by trace back
solution = ""
n = ns_len
m = we_len
while n > 0 and m > 0:
    if matrix[n][m] == matrix[n][m-1] + we[n][m-1]:
        solution += "E"
        m -= 1
    elif matrix[n][m] == matrix[n-1][m] + ns[n-1][m]:
        solution += "S"
        n -= 1
    else:
        solution += "D"
        n -= 1
        m -= 1
while n == 0 and m > 0 or n > 0 and m == 0:
    if m > 0:
        solution += "E"
        m -= 1
    else:
        solution += "S"
        n -= 1
# Solution needs to be reversed, because the traceback starts from back to start, tried it first with a recursive function, but the recursion limit was hit
solution = solution[::-1]
if args.printpath:
    print(solution)
