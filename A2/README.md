# Optimizing the administration of Atirasu

Dear APBC apprentices,

Here is your next task.

The government of the federal state Atirasu plans to modernize its administration by creating four new authorities for generally
unremarkable affairs.
These authorities shall be distributed to the capitals of eight
provinces such that each two provinces share one authority.
Consequently, the set of capitals

```
  {B,E,G,I,K,L,P,S}
```

shall be partitioned into four subsets of two elements each.

The cost of a partition is calculated as sum over the costs per
authority, where the cost per authority depends on the two assigned
cities and can be read from the following matrix (in million Euros /
year). For example, putting authority 1 in charge of the provinces
with capitals B and I costs 2 million Euros per year.

```
  8 10                     # number of capitals; cost limit
   B  E  G  I  K  L  P  S  # names of capitals
   - 10 10  2 10 10 10 10  # symmetric cost matrix
  10  -  2 10 10 10  1 10
  10  2  - 10  2  3  3  3
   2 10 10  -  4 10 10  2
  10 10  2  4  - 10 10  3
  10 10  3 10 10  -  2  2
  10  1  3 10 10  2  - 10
  10 10  3  2  3  2 10  -
```

The federal government can provide 10 million Euros per year; it wants to
know all the possible combinations that don't exceed this cost limit.

Write a program to solve this problem, place it into A2 and name it

```
  $githubname-Administration.$suffix
```

Push your solution to a new branch on GitHub, named $githubname-A2 (e.g. mtw-A2).

Your solution must be general such that it works for arbitrary (even)
numbers of cities and cost limits. Therefore read in the matrix from a
text file containing the matrix and input parameters in the format as
sketched above (without comments).

The output must list the solutions. For each solution print one line
consisting of the pairs of capitals, e.g.
```
  BE GI KL SP
```

refers to the partition {{B,E},{G,I},{K,L},{P,S}}. Obviously each
output line could be permuted such that

```
  GI LK PS BE
```

still describes the same partition. Avoid to report partitions more
than once and make your output unique by printing only the
lexicographically smallest string that describes each partition.

When given the flag -o, the program must optimize the cost (instead
of enumerating). The cost limit should be used as initial bound. As
result it must simply print the score of the best solution.


Hints:
------

* This assignment asks for solving a combinatorial optimization
  problem, which suggests a branch-and-bound strategy. Already in the
  first part, one should apply this strategy (with the simplification
  that the bound does not have to be adapted with every new solution.)
* One can assume in the code that the city names in the input are
  given in alphabetic order

Happy hacking!
