from importlib.resources import path
from re import L
import numpy as np
import sys

##the actual function via matrix storing the optimal values
def manhattan(down,left,n,m,*d):
    solution = np.zeros((n,m))
    
    for i in range(1,n):
        solution[i,0] = solution[i-1,0] + down[i-1,0]
    for j in range(1,m):
        solution[0,j] = solution[0,j-1] + left[0,j-1]
    for i in range(1,n):
        for j in range(1,m):
            if diag_toggle:
                solution[i,j] = max(solution[i-1,j]+down[i-1,j],solution[i,j-1]+left[i,j-1],solution[i-1,j-1]+d[0][i-1,j-1])
            else:
                solution[i,j] = max(solution[i-1,j]+down[i-1,j],solution[i,j-1]+left[i,j-1])
    return solution, round(solution[n-1,m-1],2)

##obtain the solution - backtracking
def traceback(sol,down,left,n,m,*d):
    path = []
    while(n>0 or m>0):
        if sol[n,m] == sol[n-1,m]+down[n-1,m] and n>0 and m>0:
            path.insert(0,"S")
            n-=1
        elif sol[n,m] == sol[n,m-1]+left[n,m-1] and n>0 and m>0:
            path.insert(0,"E")
            m-=1
        elif diag_toggle and sol[n,m] == sol[n-1,m-1] + d[0][n-1,m-1]:
            path.insert(0,"D")
            m-=1
            n-=1
        elif n==0:
            for k in range(0,m):
                path.insert(0,"E")
            m=0
        else:
            for k in range(0,n):
                path.insert(0,"S")
            n=0
    path = "".join(path)
    return path

##turns the string list into a list of floats
def float_append(matrix,val_string):
    matrix.append([float(x) for x in val_string.split()])


def file_reader(file_name):
    with open(file_name,"r") as test:
        line_length = 0
        north_south = []
        east_west = []
        if diag_toggle:
            diagonals = []
        for line in test:
            line.strip()

            if line.startswith("#") or line.startswith("\n"):
                continue 

            elif line_length != len(line) and len(north_south) == 0:
                line_length = len(line)
                float_append(north_south, line)

            elif line_length == len(line) and len(east_west) == 0:
                float_append(north_south, line)

            elif line_length != len(line) and len(east_west) == 0:
                line_length = len(line)
                float_append(east_west, line)

            elif line_length == len(line) and len(east_west) != len(north_south)+1:
                float_append(east_west, line)

            else:
                float_append(diagonals, line)

        north_south = np.asarray(north_south, dtype = np.float32)
        east_west = np.asarray(east_west, dtype = np.float32)
        if diag_toggle:
            diagonals = np.asarray(diagonals, dtype = np.float32)
            return north_south, east_west, diagonals
        else:
            return north_south, east_west

def input_verifier():
      if len(sys.argv)<2 or len(sys.argv)>4:
            print("Please provide the correct arguments! \n  file.py -t(optional) -d(optional) input_file.%txt")
   ## make sure that the file name is in the last position  
      elif len(sys.argv)>2 and (("-d" or "-t") in sys.argv[-1]):
            print("Please provide the correct arguments! \n  file.py --t(optional) -d(optional) input_file.%txt")
      else:
            return True

if __name__ == "__main__":

    if input_verifier():

        arguments = sys.argv
        file_name = arguments[-1]
        diag_toggle = False
        path_toggle = False
       
        if "-d" in arguments:
            diag_toggle = True
        if "-t" in arguments:
            path_toggle = True


    #the two matrices
        value_matrices = file_reader(file_name)
        north_south = value_matrices[0]
        east_west = value_matrices[1]
        rows = east_west.shape[0]
        columns = north_south.shape[1]

        if diag_toggle:
            diagonal_values = value_matrices[2]
            path_score_diag = manhattan(north_south,east_west, rows, columns, diagonal_values)
            print(path_score_diag[1])
            if path_toggle:
                print(traceback(path_score_diag[0],north_south,east_west,rows, columns, diagonal_values))
        else:
            path_score = manhattan(north_south,east_west, east_west.shape[0],north_south.shape[1])
            print(path_score[1])
            if path_toggle:
                print(traceback(path_score[0],north_south,east_west,rows-1, columns-1))

            

        


