# Imports
import sys
import numpy as np
from itertools import combinations


# Read Data and Store in Values and Matrix
def read_data(filename):
    nr_cap = 0  # first line first entry
    cost_limit = 0  # first line second entry
    line_ind = 0
    matrix = []
    f = open(filename, 'r')
    for line in f:
        if line_ind == 0:
            line = line.strip().split()
            nr_cap = int(line[0])
            cost_limit = int(line[1])
            line_ind = 1
        elif line_ind == 1:
            capital_ids = [x for x in line.strip().split()]
            line_ind = 2
        else:
            line = line.strip().split()
            row = [i for i in line]
            matrix.append(row)
    f.close()
    return np.array(matrix), capital_ids, nr_cap, cost_limit


# Convert Capital Combination String to a pair of ids for thge matrix
def convert_str_to_id(reference, inp):
    ref = np.array(reference)
    ind_1 = np.where(ref == inp[0])
    ind_2 = np.where(ref == inp[1])

    i = int(ind_1[0])
    j = int(ind_2[0])
    return i, j


# Get the cost of the Capital Combination ids from the Matrix
def get_cost(ref, capital, matrix):
    i, j = convert_str_to_id(ref, str(capital))
    val = matrix[i][j]
    return int(val)


# Branch and Bound Trial
def branch_and_bound(capital_candidates, capitals, nr_cap, cost_limit, cost_dict, optimize):
    # Initialize Variables
    best = np.Inf
    res = []
    res_opt = []
    tree = dict()

    for i in capital_candidates:
        if i not in tree:
            tree[i] = cost_dict[i]

        # Create Branches of tree
        next_branch = dict()

        for path in tree:
            used_capitals = []
            paths = path.split(" ")

            # Keep track of Assigned Capitals
            for city in paths:
                used_capitals.append(city[0])
                used_capitals.append(city[1])

            if i[0] not in used_capitals and i[1] not in used_capitals:

                # Update cost
                updated_cost = tree[path] + cost_dict[i]

                # Add to path and sort
                temp = paths + [i]
                new_path = sorted(temp)
                next_node = str(new_path[0])

                for j in new_path[1:]:
                    next_node += " " + j

                # Optimize if wanted
                if len(new_path) == nr_cap / 2:
                    if optimize:
                        if updated_cost < best:
                            best = updated_cost
                            res_opt = []
                            res_opt.append(next_node)
                        elif updated_cost == best:
                            res_opt.append(next_node)

                    # Else if, save all results that are feasible
                    elif updated_cost <= cost_limit and next_node not in res:
                        res.append(next_node)

                # Save next nodes
                if updated_cost <= cost_limit and len(new_path) <= nr_cap / 2:
                    if next_node not in next_branch and next_node not in tree:
                        next_branch[next_node] = updated_cost

        # Get next nodes and Update dict
        for n in next_branch:
            if n not in tree:
                tree[n] = next_branch[n]

    result = sorted(res_opt) if optimize else sorted(res)

    return result


# System Arguments
optimize = False
for i in sys.argv:
    if i.lower() == '-o':
        optimize = True
    else:
        filename = i

# Preparation
matrix, cap_ids, nr_cap, cost_limit = read_data(filename)

# Get unique combinations of capitals without repitition
c = list(combinations(cap_ids, 2))
combos = [''.join(x) for x in c]
unique_combos = np.unique(combos)

# Store Costs in a dictionary, if they are smaller than the cost-limit
cost_dict = dict()
for cap in unique_combos:
    cost = get_cost(cap_ids, cap, matrix)
    if cost >= cost_limit:
        continue
    else:
        if cap not in cost_dict:
            cost_dict[cap] = cost

capital_candidates = list(cost_dict.keys())  # keys in dictionary
res = branch_and_bound(capital_candidates, cap_ids, nr_cap,
                       cost_limit, cost_dict, optimize)

# Print Results as specified by excercise
for i in range(len(res)):
    print(res[i])
