import copy
import random
import sys

def input_verifier():
    if len(sys.argv) != 6:
        print("Please provide the correct arguments! \n  file.py -N [int] -k [int] input_file.%txt")
   ## make sure that the file name is in the last position  
    elif len(sys.argv)>2 and (sys.argv[-1].isdigit() or (sys.argv[-1] == ("-N" or "-k"))):
        print("Please provide the correct arguments! \n  file.py -N [int] -k [int] input_file.%txt")
    else:
        return True

def get_sequence(file):
    with open(file,"r") as input:
        seq = input.readline().strip()
    return seq


### generates the (k-1)-lets of every subsequence
def node_generator(sequence, k):
    nodes = []
    for i in range(0, len(sequence)-k+1):
        nodes.append(sequence[i : i+k-1])
    nodes.append(sequence[-k+1:])
    return nodes

### stores all of the nodes, edges between them in the form of a dictionary
class Graph():
    def __init__(self, nodes):
        self.nodes = nodes
        self.in_degrees = {node: 0 for node in nodes}
        self.edges = self.add_edges(nodes)
        
    ### generates the edges going through the node list and connecting each node
    ### to the next one in the list 
    ### each node is a key in the dictionary and its value is a list containing all of its children
    ### so the length of this list is equal to the out degree
    def add_edges(self, nodes):
        edge_list = {}
        for i in range(0, len(nodes)-1):
            if nodes[i] not in edge_list:
                edge_list[nodes[i]] = [nodes[i+1]]
                self.in_degrees[nodes[i+1]] += 1
            else:
                edge_list[nodes[i]].append(nodes[i+1])
                self.in_degrees[nodes[i+1]] += 1
       ### if the last node in the list hasn't come up it constucts an empty list         
        if nodes[len(nodes)-1] not in edge_list:
            edge_list[nodes[len(nodes)-1]] = []
        return edge_list


### generates a random euler path
class Euler_path():
    def __init__(self,graph):
        self.node_set = list(set(graph.nodes))
        random.shuffle(self.node_set)
        self.start_node = self.find_start(graph)
        self.full_length = len(graph.nodes)
        self.euler_path = self.find_path(copy.deepcopy(graph.edges))

    ### finds a start node
    def find_start(self, graph):
        for n in self.node_set:  #the list is shuffled so if there is no clear start node it choose on random
            node = n
            if len(graph.edges[node]) - graph.in_degrees[node] == 1:
                break
        return node
        
    def find_path(self, neighbors):
        stack = []      #keeps track of the visited nodes 
        path = []       
        node = self.start_node

        ### the algorithm goes through each node that has out-degree greater than 0, adding each in the stack
        ### and continuing with a randomly chosen neighbor from the list (and removing it)
        ### when it reaches a node without any neighbors left it adds it to the path and backtracks the stack
        ### we know that there is at least one solution (the original sequence), so there exists at least one eulerian path
        ### since a graph has an eulerian path if and only if the out-degree is equal to the in-degree of all nodes except 2 at most
        ### it can't get stuck in a node
        while(len(stack) > 0 or len(neighbors[node]) != 0 ):
            if len(neighbors[node]) != 0:
                stack.append(node)
                node = neighbors[node].pop(random.randint(0,len(neighbors[node])-1))
            else:
                path = [node] + path
                node = stack.pop(-1)

        end_path = [node] + path
        if len(end_path) == self.full_length:
            path_string ="".join(x[0] for x in end_path[0:len(end_path)-1]) + end_path[-1]
            return path_string  


if __name__ == "__main__":

    if input_verifier():

        ### input
        arguments = sys.argv
        file_name = arguments[-1]
        N = int(arguments[arguments.index("-N")+1])
        k = int(arguments[arguments.index("-k")+1])

        sequence = get_sequence(file_name)
        nodes_list = node_generator(sequence, k)
        digraph = Graph(nodes_list)

        for i in range(N):
            print(Euler_path(digraph).euler_path)
  



    

   








            
         



