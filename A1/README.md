# A1 - Word Count

Dear APBC gals and guys,

For programming warm up, here is the "Word Count" challenge:

Write a program that reads in a text (file name given on the command
line) and counts the total number of words and the number of different
words. On request, the program should print a list of the words.

"Word Count" can be written in a compiled language (e.g. C, C++,
Haskell, Java) or a scripting language (e.g. Perl, Ruby, Python).  The
program should accept the name of the text file as command line
argument.

* If option -I (for 'Ignore') is given, case shall be ignored (by
  converting all upper case to lower case, see below).

* If option -l (for 'list') is present, the program must print a list
  of words instead only counts.  This list must be sorted by word
  frequency, starting with the most common words.  ( per line print
  one word and its frequency, separated by a tab symbol; in case of
  equal frequencies, the words must be sorted alphabetically.). Please
  have a look at the example inputs and outputs; your program should
  produce outputs in exactly the same format.

To make the solutions of different class participants distinguishable
and to allow (automatic) testing, stick to the following naming scheme:
$github_name-WordCount.$suffix (e.g. mtw-WordCount.py for mtw's
solution in python).

As always, use the provided input files as test cases. Your programs should yield exactly what is given in the output files.

Copy your submission to the subdirectory A1 of our repository. Take
care to push your result in the correct branch (named like your Github
account) and place a pull request.  Then, all remaining issues can be
discussed via Github.

Hints:
------

- Ignore all punctuations and other special symbols---e.g.
  '.?!%^()-_+ etc. These symbols always separate words.  To work for
  us, the list must comprise  at least all symbols occurring in the
  test data. For example, "full!?stop" counts as two words.

- In case of option '-I', ignore upper/lowercase for counting, e.g.
  The = the. For this purpose just convert upper case to lower case.

- Make sure that your program understands calls like
```
mtw-WordCount.py dateiname
mtw-WordCount.py -I dateiname
mtw-WordCount.py -l -I dateiname
```

- Recommended data structures:
  'Dictionary' (or 'hash') in Python, Perl, Ruby; C++ has maps (STL)
  for the same purpose
  e.g. http://www.cprogramming.com/tutorial/stl/stlmap.html; C
  programmers are on their own;)


Happy hacking!
