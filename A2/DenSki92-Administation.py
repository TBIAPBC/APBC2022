import numpy as np

with open("data1.in", "r") as file_data:
    matrix = [line.split() for line in file_data]

cost = int(matrix[0][1])

matrix = matrix[1:]
cities = matrix[0]
array = np.array(matrix)
city_pairs2 = []
for i in range(len(cities) - 1):
    for j in range(i + 1, len(cities)):
        city_pairs2.append(cities[i] + cities[j])

solution = []


def path_cost(path, matrix):
    total_cost = 0
    for pair in path:
        pair1_idx = matrix[0].index(pair[0])
        pair2_idx = matrix[0].index(pair[1]) + 1
        pair_cost = array[pair2_idx, pair1_idx]

        total_cost += int(pair_cost)
    return total_cost

def best_cost(all_solutions, matrix):
    best_cost = 999
    best_solution = ""
    for solution in all_solutions:
        cost = path_cost(solution, matrix)
        if path_cost(solution, matrix) < best_cost:
            best_solution = solution
            best_cost = cost

    return best_solution, best_cost

def rec(vis, unvis):
    global solution
    for pair in unvis:
        new_vis = vis + [pair]
        new_unvis = []
        for base_pair in unvis:
            if pair[0] in base_pair or pair[1] in base_pair:
                continue
            else:
                new_unvis.append(base_pair)
        total_cost = path_cost(new_vis, matrix)

        if total_cost > cost:
            continue
        if len(new_vis) == len(cities) / 2:
            new_vis_add = new_vis
            new_vis_add.sort()
            if new_vis_add not in solution:
                solution.append(new_vis_add)

        if not new_unvis:
            return
        rec(new_vis, new_unvis)


rec([], city_pairs2)
print(solution)
print(best_cost(solution, matrix))
