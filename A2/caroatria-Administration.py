#caroatria solution attempt for assignment 2
#not yet able to sotre which capitals already used

import linecache
import sys
from itertools import combinations

selected_option = False
if sys.argv[1] == "-o":
    selected_option = True
    filename = sys.argv[2]
else:
    filename = sys.argv[1]

with open(filename) as f:
    cost_per_combo={} #dictionary to store the data
    number_capitals, cost_limit = f.readline().split()
    content = f.readline().split()
    for capital in content:
        line = f.readline().split()
        for iterator in range(len(content)): #iterates through the capitals (letters)
            if capital is not content[iterator]: #to avoid calling the same capital twice
                combinations = [capital,content[iterator]] #list of unique capital combinations
                cost_per_combo[tuple(combinations)]=(line[iterator]) #stores the combinations as keys and costs as values
f.close()

def authority_allocator(cost_per_combo,cost_limit):
    final_list = [(0,0)]
    already_listed =[]
    authority_counter = 0
    for cost in cost_per_combo:
        if authority_counter < 8:
            i=0
            j=0
            while i < len(cost):
                while j < len(cost):
                    if cost[i] not in final_list[j]:
                        final_list.append(cost)
                        authority_counter += 1
                        #j +=1
                    else:
                        already_listed.append(cost)
                    j +=1
                    i+=1
    final_list.pop(0)
    solution = list(set(final_list)-set(already_listed))
    print(solution)


if selected_option:
    print("option -o chosen")
else:
    authority_allocator(cost_per_combo,cost_limit)