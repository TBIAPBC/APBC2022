#caroatria solution attempt for assignment 2
#printing the capital letters does not yet work

from dataclasses import replace
import linecache
import sys
from itertools import combinations

selected_option = False
if sys.argv[1] == "-o":
    selected_option = True
    filename = sys.argv[2]
else:
    filename = sys.argv[1]
matrix_list=[]


with open(filename) as f:
    next(f)
    next(f)
    for line in f:
        content = line.split()
        matrix_list.append(content)
    capital_letters = linecache.getline(filename,2).strip("\n")


f.close()
for i in range(len(matrix_list)):
    matrix_column = matrix_list[i]
    for j in range(len(matrix_list)):
        if matrix_column[j] == '-':
            matrix_column[j] = 0 #to get rid of the "-" character and to facilitate the computational steps later on
        else:
            matrix_column[j] = int(matrix_column[j])
    matrix_list[i] = matrix_column
for capital in capital_letters:
    if capital.isalpha():
        capital_index_list = capital_letters.index(capital)
        #print(capital_index_list)

def get_combos(list_name):
    #list(combinations.enumerate,list_name)
    cost_pairs=[]
    pairs = [x for x in combinations(list_name, 2) ]
    # b = list((i,j) for ((i,_),(j,_)) in pairs)
    # print(b)
    for x in pairs:    
        if x[0] + x[1]<=10:
            cost_pairs.append(x)
    return authority(cost_pairs)

def authority(cost_pairs):
    authority = []
    authority_counter = 0
    for combination in cost_pairs:
        if authority_counter > 4:
            break
        elif authority_counter == 0:
            authority.append(combination)
            authority_counter += 1
        else:
            if combination[0] or combination[1] in authority:
                break
            else:
                authority.append(combination)
                authority_counter += 1
    return(authority)  

if selected_option:
    print("option -o chosen")
else:
    for i in range(len(matrix_list)):
        get_combos(matrix_list[i])