#caroatria 11835854

import sys
def longest_path(n, m, vertical, horizontal,chosen_option="off"):
    cost = [[0]*(m+1) for _ in range(n+1)]
    for i in range(1, n+1):
        cost[i][0] = cost[i - 1][0] + vertical[i - 1][0]
    for j in range(1, m+1):
        cost[0][j] = cost[0][j - 1] + horizontal[0][j - 1]
    for i in range(1, n+1):
        for j in range(1, m+1):
            cost[i][j] = max(cost[i - 1][j] + vertical[i - 1][j], cost[i][j - 1] + horizontal[i][j - 1])
    if chosen_option == "-t":
        print(path_finder(cost,n,m))
        print(cost[n][m])
    else:
        print(cost[n][m])
    return(cost[n][m])

def path_finder(cost,n,m):
    path =[]
    while(m>0 and n>0):
        if cost[n-1][m] > cost[n][m-1]:
            path.insert(0,"S")
            n -=1
        else:
            path.insert(0,"E")
            m -=1
    if m==0:
        path.insert(0,"S")
    else:
        path.insert(0,"E")
    path_string = "".join([str(letter) for letter in path])
    return(path_string)
    


def file_reader(filename):
    weight_horizontal=[]
    weight_vertical=[]
    weight_diagonal =[]
    with open(filename,"r") as f:
        l = [[int(num) for num in line.split()] for line in f if not line.strip().startswith("#")]
        lenght_horizontal = len(l[0])
        list_length = len(l)
        counter=0
        for counter in range(list_length):
            if len(l[counter]) == lenght_horizontal:
                weight_horizontal.append(l[counter])
            if len(l[counter]) != lenght_horizontal:
                lenght_vertical = len(l[counter])
                if len(l[counter]) == lenght_vertical:
                    weight_vertical.append(l[counter])
                if len(l[counter]) != lenght_vertical:
                    length_diagonal = len(l[counter])
                    if len(l[counter]) == length_diagonal:
                        weight_diagonal.append(l[counter])
        n=len(weight_vertical)-1
        m=lenght_horizontal-1
    return(n,m,weight_horizontal,weight_vertical)
chosen_option="off"
if len(sys.argv) > 2:
    filename=sys.argv[2]
    chosen_option= sys.argv[1]
    print(filename)
else:
    filename=sys.argv[1]

if __name__ == "__main__":
    n, m, vertical_matr, horizontal_matr = file_reader(filename)
    longest_path(n, m, vertical_matr, horizontal_matr,chosen_option)