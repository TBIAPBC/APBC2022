import sys
import numpy as np

def SolOutput(pairs):  # prints one line of output
    for tuples in pairs:
        for element in tuples:
            print(element, end="")
        print(" ", end="")
    print("")


def PairCost(a,b, costM, capitals):  # function that returns the cost for assigning an authority to the two cities a and b
    aindex = capitals.index(a)
    bindex = capitals.index(b)
    cost = costM[aindex,bindex]
    return cost

def ListCost(L, costM, capitals):  # function that returns the cost for a list of tuples
    cost = 0
    for tuple in L:
        cost = cost + PairCost(tuple[0], tuple[1], costM, capitals)
    return cost

def administration(paired, rest, costM, costlimit):
    #print("rest = ", rest)
    #print("paired = ", paired)
    #sol = []
    if len(rest)==0:
        SolOutput(paired)
        return
    elif len(rest)==2:
        if ListCost(paired, costM, capitals) + PairCost(rest[0], rest[1], costM, capitals) <= costlimit:
            paired.extend([rest])  # extend is like append except it does not give a nested list of lists
            SolOutput(paired)
            #print("rest added: ", rest)
        return
    else:
        for i in np.arange(1,len(rest)):
            # only keep working on list with this pair (rest[0], rest[i] IF adding this pair does not make the solution go over the cost limit:
            if ListCost(paired, costM, capitals) + PairCost(rest[0], rest[i], costM, capitals) <= costlimit:
                paired_2 = paired.copy()  # need extended paired for recursive call, but for next for-loop iteration want to undo, therefore copy
                paired_2.extend([[rest[0],rest[i]]])  # add the tuple (0,i) from rest
                #print("pair extend: ", [[rest[0], rest[i]]])
                rest_2 = rest[1:i]  # need an extra variable, since x.extend() always returns None
                rest_2.extend(rest[i+1:])  # rest without element 0 and without element i
                #sol.extend([administration(paired_2, rest_2, costM, costlimit)])
                administration(paired_2, rest_2, costM, costlimit)
                #print("    sol = ", sol)
        return
        #return sol





# ---- READING IN THE DATA: ------

optim = False  # True if -o is given as argument

args = sys.argv
assert len(args)>=2, "Both the python script and the text-input file must be provided!"
if len(args)>2:
    if '-o' in args:
        optim = True
    else:
        print("Warning: Unknown flag was given and is being ignored.")

f = open(sys.argv[-1], "r")  # read in the input (file is the last argument)
input1 = f.read()
f.close()


input_split=input1.split()  # input split by spaces, get 1D list.
# We know what format the input will take: First two elements of list are number of capitals and cost limit.
# Next nCapitals symbols are the name of the capitals. Next nCaptials x nCapitals symbols is the cost matrix.
nCapitals = int(input_split[0])  # number of capitals (n of nxn matrix)
costlimit = int(input_split[1])  # cost limit
capitals = input_split[2:2+nCapitals]  # list of capitals

costM = np.zeros([nCapitals, nCapitals])  # initialize cost Matrix
#print(input_split[2+nCapitals])  # the first '-', start of cost matrix

#define cost matrix:
for i in np.arange(0,nCapitals):
    for j in np.arange(0,nCapitals):
        if i==j:
            costM[i,j]=None
        else:
            #I want to create a matrix out of a list. I know the dimensions of the matrix is [nCapitals, nCapitals].
            #2+nCapitals is starting point [0,0]. To get correct row, multiply desired row i with number of columns to
            #get to the correct position in the list. To get the correct column, just add the desired column j.
            #(thinking it through with a smaller matrix can help)
            costM[i,j]=input_split[2+nCapitals+nCapitals*i+j]
#print("costM =")
#print(costM)

#List = [['B','K'], ['E', 'G']]
#print("ListCost(BK, EG) = ", ListCost(List, costM, capitals))

# --- FINISHED READING IN THE DATA -----

#print("PairCost(E,G) = ", PairCost("E","G",costM,capitals))
#capitals=["1","2","3","4","5","6","7","8"]
administration([], capitals, costM, costlimit)