from itertools import combinations
import argparse

parser = argparse.ArgumentParser(description='Administration',
                                 usage="""
                                 use "%(prog)s --help" for more information
                                     """,
                                 formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument('administration_in')

parser.add_argument("-o", "--optimized_cost", help="""
    load it with:filename.py -o Administration-test1.in

   
                      """, action="store_true")

args = parser.parse_args()


with open(args.administration_in, "r") as text:
    first_line = text.readline().split()
    cap_number = int(first_line[0])
    cost_limit = int(first_line[1])
    letters_of_capitals = text.readline().split()
    city_combinations = combinations(letters_of_capitals, 2)
    cost_matrix = []
    cost_of_city_pairs = {}
    for i in range(0, cap_number):
        cost_matrix.append(text.readline().split())

    for tuple in city_combinations:
        cost_of_city_pairs[tuple] = int(cost_matrix[letters_of_capitals.index(tuple[0])][letters_of_capitals.index(tuple[1])])


def administration(cost_of_city_pairs, cost_limit, solution, letters_of_capitals, interm_cost):
    global minimum_cost


    if len(letters_of_capitals) % 2 == 0 and not len(letters_of_capitals) == 2:
        administration(cost_of_city_pairs, cost_limit, solution + [letters_of_capitals[0]], letters_of_capitals[1:], interm_cost)

    elif len(letters_of_capitals) == 2:
        if interm_cost + cost_of_city_pairs.get((letters_of_capitals[0], letters_of_capitals[1])) <= cost_limit:
            interm_cost += cost_of_city_pairs.get((letters_of_capitals[0], letters_of_capitals[1]))
            if args.optimized_cost and interm_cost < minimum_cost:
                minimum_cost = interm_cost
            elif not args.optimized_cost:
                solutions.append(solution + [letters_of_capitals[0], letters_of_capitals[1]])
    else:
        for el in letters_of_capitals:
            if interm_cost + cost_of_city_pairs.get((solution[-1], el)) <= cost_limit:
                new_unvisited = letters_of_capitals.copy()
                new_unvisited.remove(el)
                if args.optimized_cost and interm_cost + cost_of_city_pairs.get((solution[-1], el)) <= minimum_cost:
                    administration(cost_of_city_pairs, cost_limit, solution + [el], new_unvisited, interm_cost + cost_of_city_pairs.get((solution[-1], el)))
                elif not args.optimized_cost:
                    administration(cost_of_city_pairs, cost_limit, solution + [el], new_unvisited, interm_cost + cost_of_city_pairs.get((solution[-1], el)))

    return solutions


intermediate_cost = 0
solutions = []
minimum_cost = cost_limit

administration(cost_of_city_pairs, cost_limit, solutions, letters_of_capitals, intermediate_cost)


for sol in solutions:
    end_list = ["".join(el) for el in zip(sol[::2],sol[1::2])]
    print(*end_list, sep=" ")

if args.optimized_cost:
    print(minimum_cost)