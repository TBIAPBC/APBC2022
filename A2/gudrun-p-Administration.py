import sys
import numpy as np

# ---- READING IN THE DATA: ------

f = open(sys.argv[1], "r")  # read in the input
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
print(costM)

# --- FINISHED READING IN THE DATA -----

