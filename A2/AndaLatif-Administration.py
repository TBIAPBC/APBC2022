#Latif Anda Ramona
# 01046290
import sys

def read_from_file(ifn):
    f = open(ifn, 'r')   
    no_of_capitals , cost_limit = f.readline().split()
    cost_limit = int( cost_limit)
    capitals = f.readline().split()
    cost = {}
    for cap in capitals:
        line = f.readline().split()
        for i in range(len(capitals)):
            if cap != capitals[i]:
               cost[tuple(sorted([cap,capitals[i]]))] = int(line[i]) #since the matrix is symetric
    f.close()
    return  int(no_of_capitals) , cost_limit, capitals, cost

def Generate_authorities( partial_res, cost_limit, cost, unvisited, opt):
    global optimum
    global res
    if unvisited == []:
        if (len(partial_res) == no_of_capitals) and (cost_limit >= optimum):
            if opt == "-o":
                if cost_limit > optimum:
                        optimum = cost_limit
                        res = []
            current = []
            for i in range(len(partial_res)-1):
                if i % 2 == 0:
                   current.append("".join(sorted([partial_res[i], partial_res[i+1]])))
            current=" ".join(current)       
            if not(current in res):
                res.append(current)
            return  res, partial_res
    
    if cost_limit < optimum: #throw away
       return 
    
    if len(partial_res) % 2 == 0: ##even, just start with the first still unvisited
                if unvisited == []:
                    return
                Generate_authorities( partial_res + [unvisited[0]], cost_limit, cost, unvisited[1:], opt)
    else:
         for i in range(len(unvisited)): ##odd, pair with all others 
            curr_cost = cost_limit - cost[tuple(sorted([partial_res[-1], unvisited[i]]))]
            if  curr_cost >= 0:
                    Generate_authorities( partial_res + [unvisited[i]],  curr_cost, cost, unvisited[:i] + unvisited[i+1:], opt)
 
if __name__ == '__main__':
    arg = sys.argv[0:]   
    if (len(arg) == 1):
        print("Please run again providing an input file name")
    if (len(arg) > 3):
         print("Too many arguments. Please run again providing maximally the option -o and one input file name")
    else:
        ifn = arg[-1]
        opt = arg[-2]
        if opt != "-o" :
            if not "." in opt:
                print("option " + opt + " was ignored, only -o is a valid option")
                opt=""
        ifn = arg[-1]
        out = open(ifn.split(".")[0] + ".out", 'w')
        no_of_capitals , cost_limit, capitals, cost = read_from_file(ifn)
        res = []
        optimum = 0
        Generate_authorities( [], cost_limit, cost, capitals, opt)
        
        if opt == "-o" :
            c=0
            for pair in res[0].split(" "):                
                c=c + cost[tuple(pair)]                
            print(c)
            out.write(str(c)+"\n")
        else:
            out.write("\n".join( list for list in res))
            out.write("\n")
        out.close()
        print(ifn.split(".")[0]+".out contains the output")