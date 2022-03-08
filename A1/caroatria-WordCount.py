#!/usr/bin/python
import sys
import re

def sorting_function (dict):
    sort_by_key = {k:v for (k,v) in sorted(dict.items())}
    sorted_dict = sorted( sort_by_key.items(), key=lambda item: item[1], reverse=True) 
    return sorted_dict

def ignore_special_char (text):
    global new_file_content
    new_file_content = re.sub(r"[.?!%^()-_+]", " ", text)
    return new_file_content

def word_count(option, filename):
    f = open(filename, "r")
    file_content = (f.read())
    new_file_content = ignore_special_char(file_content)
    if (option == "-l"):
        counts = dict()
        word_list= new_file_content.split() 
        for word in word_list:
            if word in counts:
                counts[word] += 1
            else:
                counts[word] = 1
        for k,v in sorting_function(counts):
            word_frequency = (str(k) + "\t" + str(v))
            print(word_frequency)
    elif (option ==  "-I"):
        counts = dict()
        word_list= new_file_content.lower().split()
        print(word_list)
        for word in word_list:
            if word in counts:
                counts[word] += 1
            else:
                counts[word] = 1
        number_of_words = len(counts)
        print(str(len(word_list)) + "/" + str(number_of_words))
    else:
        counts = dict()
        word_list= new_file_content.split() 
        for word in word_list:
            if word in counts:
                counts[word] += 1
            else:
                counts[word] = 1
        number_of_words = len(counts)
        f.close()
        print(str(len(word_list)) + "/" + str(number_of_words))

def option_function (name_of_script):
    if (name_of_script == "-l" or name_of_script == "-I"):
        word_count(sys.argv[1],sys.argv[2])
    else:
        word_count("no option",sys.argv[1])

option_function(sys.argv[1])