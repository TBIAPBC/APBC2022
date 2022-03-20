import sys
import pandas as pd
from itertools import combinations

# read in data and check for optimization option
optimize = False

for i in range(len(sys.argv)):
    if sys.argv[i] == "-o":
        optimize = True
    else:
        filename = sys.argv[i]

file = open(filename)


line_count = 0
matrix = []
for line in file:
    if line_count == 0:
        firstline = line.split()
        capital_nr = int(firstline[0])
        cost_limit = int(firstline[1])
        line_count += 1

    elif line_count == 1:
        header = line.split()
        line_count += 1

    else:
        elements = line.split()
        matrix.append(elements)


for i in range(len(matrix)):
    matrix_row = matrix[i]
    for j in range(len(matrix)):
        if matrix_row[j] != '-':
            matrix_row[j] = int(matrix_row[j])

    matrix[i] = matrix_row


data = pd.DataFrame(matrix, index=header, columns=header)


# create all possible combinations of capitals
subsets = combinations(header, 2)

subset_list = []
for s in subsets:
    subset_list.append(s)


def capital_check(pairs, new_pair, loop_count):
    """
    function to check if a capital is already assigned to an authority
    :param pairs: all current pairs of a branch
    :param new_pair: pair to be added to the branch
    :param loop_count:
    :return: allowed - True, if the cities in the new pair are not already in the other pairs of the branch

    """


    allowed = True
    capitals = []

    if loop_count == 1:
        for p in pairs:
            capitals.append(p)

    else:
        for p in pairs:
            capitals.append(p[0])
            capitals.append(p[1])

    for city in new_pair:
        if city in capitals:
            allowed = False

    return allowed



def lexicographic_order(pairs, new_pair):
    """
    function to make sure not to have the same combination of cities in a different lexicographic order
    :param pairs: all current pairs of a branch
    :param new_pair: pair to be added to the branch
    :return: allowed - True, if the pair to be added is lexicographically greater than the others
    """

    allowed = True

    if type(pairs) is tuple:
        if pairs[0] >= new_pair[0]:
            allowed = False

    else:
        for i in range(len(pairs)):
            selected_pair = pairs[i]

            if selected_pair[0] >= new_pair[0]:
                allowed = False


    return allowed



def branchandbound(solutions_list, subset_list, cost_list, data, loop_count):
    """

    :param solutions_list: contains all branches of city combinations which could be solutions
    :param subset_list: contains all possible combinations of cities
    :param cost_list: contains corresponding cost of a branch
    :param data: cost matrix
    :param loop_count: number of loops, corresponds to number of city combinations in a branch
    :return:    solution - list of all combinations which are a solution
                cost - cost corresponding to the solution
    """

    if loop_count == capital_nr/2:
        sol_list = solutions_list
        cost = cost_list
        return sol_list, cost

    else:
        new_solutions_list = []
        new_cost_list = []
        for i in range(len(solutions_list)):
            for pair in subset_list:
                if lexicographic_order(solutions_list[i], pair):
                    if capital_check(solutions_list[i], pair, loop_count):

                        sum = cost_list[i] + data.at[pair[0], pair[1]]
                        if sum <= cost_limit:
                            new_element = []
                            if type(solutions_list[i]) is tuple:

                                new_element.append(solutions_list[i])
                            else:
                                for s in solutions_list[i]:
                                    new_element.append(s)

                            new_element.append(pair)

                            new_solutions_list.append(new_element)

                            new_cost_list.append(sum)



        solutions_list = new_solutions_list

        cost_list = new_cost_list
        loop_count += 1

        solution, cost = branchandbound(solutions_list, subset_list, cost_list, data, loop_count)
        return solution, cost


# create list with costs corresponding to each pair to be consistent with the format used in the function
first_cost_list = []

for pair in subset_list:
    cost = data.at[pair[0], pair[1]]
    first_cost_list.append(cost)

loop_count = 1

# apply branch and bound function
sol_list, cost_list = branchandbound(subset_list, subset_list, first_cost_list, data, loop_count)


# print output
if optimize:
    print(min(cost_list))

else:
    for line in sol_list:
        string = ""
        first = True
        for pair in line:
            if first:
                add_string = pair[0] + pair[1]
                first = False

            else:
                add_string = " " + pair[0] + pair[1]
            string += add_string
        print(string)