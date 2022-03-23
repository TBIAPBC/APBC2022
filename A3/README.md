Write a program to solve the following tasks by dynamic programming.

The Manhattan Tourist Problem:
------------------------------

The street network of Manhattan has the form of a grid. Our tourist values streets (from crossing to crossing) by the number of sights along them.

```
       start here
       |
       v
       +--3--+--3--+
       |     |     |
       1     6     2
       |     |     |
       +--3--+--2--+
       |     |     |
       4     0     7
       |     |     |
       +--5--+--7--+
                   ^
                   |
                  end here
```

The problem is to find a path from the top left to the bottom right corner of the grid with maximum weight. In each step, the tourist moves either to the east or to the south.

Your program must read in the weights from a file (and, naturally shall work for arbitrary grid sizes). For
the above grid, the file looks as follows

```
     # size (north-south dimension times west-east dimension)
     # 3 3
     # north-south streets
     1 6 2
     4 0 7
     # west-east streets
     3 3
     3 2
     5 7
```

The input should be allowed to contain decimal numbers (with maximally 2 digits after the comma), empty lines and arbitrary comments; therefore, your program must ignore all comments in the input (the comments start with the '#' symbol and extend to the end of the line).

A slight enhancement is to also consider diagonal edges between vertices. As you can expect, we need additional input for that. In particular, a (N-1)\*(N-1) matrix containing diagonal edge weights. A real-world input file on a 5*5 grid containing vertical, horizontal and diagonal edge weight could look like this

```
#G_down: 4 5
  0.60   0.65   0.91   0.94   0.14
  0.85   0.27   0.70   0.31   0.63
  0.63   0.23   0.35   0.77   0.20
  0.37   0.76   0.41   0.30   0.67
#---
#G_right: 5 4
  0.76   0.41   0.72   0.13
  0.57   0.64   0.62   0.62
  0.37   0.98   0.36   0.24
  0.99   0.77   0.39   0.35
  0.37   0.34   0.62   0.82
#---
#G_diag: 4 4
  6.74   7.03   2.47   6.25
  4.48   3.75   2.98   3.62
  7.90   3.63   3.67   3.18
  9.30   8.40   9.02   2.58
#---
```

Your program should be able to process both horizontal/vertical (HV) and horizontal/vertical/diagonal (HVD) input files and print the weight of the maximum path for a given input file to STDOUT. Implement a switch -d, which lets the program process input files that do not only contain HV, but also diagonal edge weights. Given option -t, the program should additionally print the best path. In our example, the calls (for my C program) and respective
output should thus look like

```
    > mtw-Manhattan Manhattan-testHV1.in
    18
```

and

```
    > mtw-Manhattan -t Manhattan-testHV1.in
    18
    ESES
```

where 'E' means move to east and 'S', move to south; the moves are reported in the order from start to end. (If several maximum paths should be possible, our tourist always prefers going to the south!)

A sample call for the version considering also diagonal weights should look like

```
   > mtw-Manhattan -d Manhattan-testHVD1.in
```

Here, let 'D' denote a diagonal step in the traceback.

Hints:

  * Implement a 2D DP matrix that stores the optimal path weight from the start to each crossing (or corner). The final result is computed at the end corner. The path is obtained by trace back.

** This assignment is due on 5 April 2022 10AM **

Happy hacking!
