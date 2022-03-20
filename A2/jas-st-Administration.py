import sys
from itertools import combinations

def read_input(file):
      with open(file,"r") as text:
            first_line = text.readline().split()
            cap_number = int(first_line[0])
            cost_lim = int(first_line[1])   
            capitals_list = text.readline().split()
            distributions = combinations(capitals_list,2) #all possible combinations of capitals distributions
            cost_matrix = []
            cost_values = {}  
            for i in range(0,cap_number):
                cost_matrix.append(text.readline().split())  #this just reads the whole matrix directly line by line

#to store the cost values more efficiently I decided on using a dictionary 
#at first i tried to use a set as the dictionary key, since the order of the capitals doesn't matter, but it is unhashable  
#the combinatons produce sorted tuples and since the cap names are sorted in alphabetical order the tuples are
#also automatically sorted

            for tuple in distributions:
                cost_values[tuple] = int(cost_matrix[capitals_list.index(tuple[0])][capitals_list.index(tuple[1])])
            
      return cost_lim, capitals_list, cost_values

def administration(cost, limit, solution, to_visit, interm_cost):
     global cost_min
     global solutions

     ##this mode means that the function is searching for the available capital to begin the pair for the next authority 
     if len(to_visit)%2==0 and not len(to_visit)==2:   
           administration(cost, limit, solution+[to_visit[0]],to_visit[1:], interm_cost)
      
      #end mode when only the last two capitals remain 
     elif len(to_visit) == 2:
            if interm_cost + cost.get((to_visit[0], to_visit[1])) <= limit:
                interm_cost += cost.get((to_visit[0],to_visit[1]))
                if optimum and interm_cost < cost_min:
                      cost_min = interm_cost     
                elif not optimum:
                      solutions.append(solution + [to_visit[0],to_visit[1]])

      #pairing mode where the function finds all capitals that produce sum less than the limit     
     else:
           for el in to_visit:
                 if interm_cost + cost.get((solution[-1],el)) <= limit:
                        new_unvisited = to_visit.copy()
                        new_unvisited.remove(el)

                        ## when the optimum mode is on, it always checks if the current sum doesn't exceed the current lowers optimal sum
                        if optimum and interm_cost+cost.get((solution[-1], el))<=cost_min:
                              administration(cost, limit, solution+[el], new_unvisited, interm_cost+cost.get((solution[-1],el)))
                        else:
                              administration(cost, limit, solution+[el], new_unvisited, interm_cost+cost.get((solution[-1],el))) 

def input_verifier():
      if len(sys.argv)<2 or len(sys.argv)>3:
            print("Please provide the correct arguments! \n  file.py -o(optional) input_file.%txt")
      elif len(sys.argv)==3 and "-o" not in sys.argv[1]:
            print("Please provide the correct arguments! \n  file.py -o(optional) input_file.%txt")
      else:
            return True
      


if __name__ == "__main__":

      if input_verifier():

            ##reading the file and assigning variables
            input_file = read_input(sys.argv[-1]) 

            cost_values = input_file[2]
            capitals_list = input_file[1]
            cost_lim = input_file[0] 

            if "-o" in sys.argv:
                  optimum = True
            else:
                  optimum = False

            begin = []  
            intermediate_cost = 0     
            cost_min = input_file[0] 
            solutions = [] 

            if optimum:
                  administration(cost_values, cost_lim, begin, capitals_list, intermediate_cost)
                  print(cost_min)
            else:
                  administration(cost_values, cost_lim, begin, capitals_list, intermediate_cost)
                  
                  for sol in solutions:
                        end_list = ["".join(el) for el in zip(sol[::2],sol[1::2])] 
                        print(*end_list, sep=" ")



