#Latif Anda Ramona
# 01046290
import argparse
from pathlib import Path

def read_file(ifn, diag):
    f = open(ifn, 'r')
    lines = []
    for line in f:
        if line.startswith("#"): #skip comment lines
            continue
        if line.strip() == "": #skip empty lines
            continue
        if '#' in line.strip(): #skip the rest of the line
            line = line[: line.index("#")]
        lines.append([float(el) for el in line.strip().split()])
    if diag:
        NS = lines[ : (len(lines)-1) // 3]    
        WE = lines[(len(lines)-1) // 3 : 2*(len(lines)-1) // 3+1 ]
        D= lines[ 2*(len(lines)-1) // 3 +1:]
        NS=[ [0 for _ in range(len(NS[0]))] ] + NS
        WE=[ [0] + line for line in WE]
        D=[ [0 for _ in range(len(D[0]))] ] + D
        D=[ [0] + line for line in D]
    else: 
        NS = lines[ : len(lines) // 2]    
        WE = lines[len(lines) // 2 : ]
        NS=[ [0 for _ in range(len(NS[0]))] ] + NS
        WE=[ [0] + WE[i] for i in range(len(WE))]    
        D=[[-float("inf") for _ in range(len(WE[0]))] for _ in range(len(NS))]
    f.close()
    return NS, WE, D

def find_path(NS, WE):
    n = len(WE[0])
    m = len(NS)
    s = [ [0 for _ in range(n)] for _ in range(m)]
    backtrack = [ [-1 for _ in range(n)] for _ in range(m)]
    for i in range(1,n):
         s[0][i] = s[0][i-1] + WE[0][i]
    for i in range(1,m):
         s[i][0] = s[i-1][0] + NS[i][0]
    for i in range(0, m):       
        for j in range(0, n):            
           if i == 0 and j == 0:
               continue           
           var1 = s[i][j-1] + WE[i][j]
           var2 = s[i-1][j] + NS[i][j]           
           if var1 > var2:
                s[i][j] = var1
                backtrack[i][j] = 0
           else:
               s[i][j] = var2
               backtrack[i][j] = 1
    return s[-1][-1],  backtrack

def find_path_D(NS, WE, D):
    n = len(WE[0])
    m = len(NS)
    s = [ [0 for _ in range(n)] for _ in range(m)]
    backtrack = [ [-1 for _ in range(n)] for _ in range(m)]
    for i in range(1,n):
         s[0][i] = s[0][i-1] + WE[0][i]
    for i in range(1,m):
         s[i][0] = s[i-1][0] + NS[i][0]
    for i in range(0, m):       
        for j in range(0, n):            
           if i == 0 and j == 0:
               continue
           elif i == 0 or j == 0:
               var=[s[i][j-1] + WE[i][j], s[i-1][j] + NS[i][j],  0]
           else:
               var=[s[i][j-1] + WE[i][j], s[i-1][j] + NS[i][j],  s[i-1][j-1] + D[i][j]]
           match var.index(max(var)):
            case 0:
                s[i][j] = var[0]
                backtrack[i][j] = 0
            case 1:
               s[i][j] = var[1]
               backtrack[i][j] = 1
            case 2:
                s[i][j] = var[2]
                backtrack[i][j] = 2
    return s[-1][-1],  backtrack
    
def reconstruct_path(path, backtrack, out):
    i = len(backtrack)-1
    j = len(backtrack[0])-1
    while i >  0 or j >  0:
        match backtrack[i][j]:
            case 0:
                path="E" + path
                j = j-1
            case 1:
                path="S" + path
                i = i-1
            case 2:
                path="D" + path
                i -= 1
                j -= 1 
    out.write(path)
    print(path)
    return     
         
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type = str, help="Enter path of input file.")
    parser.add_argument("-t", "--best_path", required = False, action="store_true", help = "Print the best path.")
    parser.add_argument("-d", "--diagonal", required = False, action="store_true", help = "diagonal weights also considered") 
     
    arg = parser.parse_args()
    ifn = Path(arg.input_file)  
    ofn = ifn.stem+ ".out"      
    out = open(ofn, "w")
    NS, WE, D = read_file(arg.input_file, arg.diagonal)
    if   arg.diagonal:
        max, backtrack = find_path_D(NS, WE, D)
    else: 
        max, backtrack = find_path(NS, WE)
    if int(max) == float(max):
            decimals = 0
    else:
            decimals = 2
    out.write('{0:.{1}f}'.format(max, decimals) + "\n")
    print('{0:.{1}f}'.format(max, decimals))
    if arg.best_path: 
        reconstruct_path("", backtrack, out)
        out.write("\n")         
    out.close()
    print("\n"+ofn + "contains the output")