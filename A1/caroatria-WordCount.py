#!/usr/bin/python
import sys
import re
import argparse



def sorting_function (dict):
    sort_by_key = {k:v for (k,v) in sorted(dict.items())}
    sorted_dict = sorted( sort_by_key.items(), key=lambda x: (-x[1], x[0]))
    return sorted_dict

def ignore_special_char (text):
    global new_file_content
    new_file_content = re.sub(r"[?!%^()-;,':\"\.]", " ", text)
    return new_file_content

def word_count(option, filename):
    f = open(filename, "r")
    file_content = (f.read())
    new_file_content = ignore_special_char(file_content)
    if (option == "-l" or option == "-both"):
        counts = dict()
        if (option == "-both"):
            word_list= new_file_content.lower().split()
            for word in word_list:
                if word in counts:
                    counts[word] += 1
                else:
                    counts[word] = 1
            for k,v in sorting_function(counts):
                word_frequency = (str(k) + "\t" + str(v))
                print(word_frequency)
        else:
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
        for word in word_list:
            if word in counts:
                counts[word] += 1
            else:
                counts[word] = 1
        number_of_words = len(counts)
        print(str(number_of_words) + " / " + str(len(word_list)))     
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
        print(str(number_of_words) + " / " + str(len(word_list)))

parser = argparse.ArgumentParser()
parser.add_argument("filename", nargs="?", type=str)
parser.add_argument("-l", "--list",  nargs ="?" , help = "create a list")
parser.add_argument("-I", "--insensitive",  nargs ="?" ,help = "caseinsensitive")
args=parser.parse_args()

if (len(sys.argv)>3):
    word_count("-both", sys.argv[3])
elif args.list:
    word_count("-l", sys.argv[2])
elif args.insensitive:
    word_count("-I", sys.argv[2])
else:
    word_count("no option", args.filename)