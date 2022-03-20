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

def administration(cost, limit, solution, unvisited, interm_cost):
     global cost_min

     ##this mode means that the function is searching for the next available capital for the next authority 
     if len(unvisited)%2==0 and not len(unvisited)==2:   
           administration(cost, limit, solution+[unvisited[0]],unvisited[1:], interm_cost)
      
      #end mode when only the last two capitals remain 
     elif len(unvisited) == 2:
            if cost.get((unvisited[0],unvisited[1])) <= limit:
                interm_cost += cost.get((unvisited[0],unvisited[1]))
                if optimum and interm_cost < cost_min:
                      cost_min = interm_cost     
                elif not optimum:
                      print("YOU WIN!!!!",solution, interm_cost)

      #pairing mode where the function finds all capitals that produce sum less than the limit     
     else:
           for el in unvisited:
                 if cost.get((solution[-1],el)) <= limit:
                        new_unvisited = unvisited.copy()
                        new_unvisited.remove(el)
                        if optimum and interm_cost+cost.get((solution[-1], el))<=cost_min:
                              administration(cost, limit - cost.get((solution[-1], el)) , solution+[el], new_unvisited, interm_cost+cost.get((solution[-1],el)))
                        else:
                              administration(cost, limit - cost.get((solution[-1], el)) , solution+[el], new_unvisited, interm_cost+cost.get((solution[-1],el))) 


if __name__ == "__main__":

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

      if optimum:
            administration(cost_values, cost_lim, begin, capitals_list, intermediate_cost)
            print(cost_min)
      else:
            print(administration(cost_values, cost_lim, begin, capitals_list, intermediate_cost))



