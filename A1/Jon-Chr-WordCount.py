# Task A1
import sys

ignorecase = False
get_list = False
command_length = len(sys.argv)
file = ""
symbols = [".",",","?","%","^","(",")","-","+","*","~","#",";","!","\"","\'",":"]


# Check for arguments
for i in range(command_length):
    if (i == 0):
        continue
    if (sys.argv[i].upper() == "-I"):
        #Ignore upper/lower case (upper to lower)
        ignorecase = True
    elif (sys.argv[i].upper() == "-L"):
        #print list of words, not only counts - sorted by word frequency (most common first)
        get_list = True
    else:
        file = sys.argv[i]

# Get WordCount
def Get_WordCount(filename, ignorecase, get_list):
    word_count = dict()
    words = 0
    diff_words = 0
    word_list = ""

    f = open(filename)
    for line in f:
        if (ignorecase == True):
            new_line = Check_Symbols(line)
            word_list += new_line.lower()
        else:
            new_line = Check_Symbols(line)
            word_list += new_line
    f.close() 

    word_list = word_list.split()
    word_list = sorted(word_list)

    for word in word_list:
        if (word in word_count):
            word_count[word] += 1
            words += 1;
        else:
            word_count[word] = 1
            words += 1;
            diff_words += 1 
            
    
    return words, diff_words, word_count

# Check for special Symbols
def Check_Symbols(word):
    new_word = ""
    for letter in word:
        if (letter in symbols):
            new_word += '\t'
        else:
            new_word += letter
    return new_word


words, diff_words, word_count = Get_WordCount(file, ignorecase, get_list)

if (get_list == True):
    length = len(file)-3
    g = open("Jon-Chr-" + file[:length] + ".out", "w")
    # Create Output file with words for simplicity 
    for key in sorted(word_count, key=word_count.get, reverse=True):
        sentence = str(key) + "\t" + str(word_count[key]) + "\n"
        g.write(sentence)
    g.close()
else:
    # Print Result to Console
    print(str(diff_words) + ' / ' + str(words))
    