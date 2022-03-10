import sys
import re

def main():
    ###checks if the commands are listed right 
    if len(command_list)>=3 and not (any(x in ["-l","-I"] for x in command_list[1:len(command_list)-1])):
        print("Please use a valid notation! \n python script.py -l(optional) -I(optional) input_file.%txt")
    else:
        Word_Counter()

def Word_Counter():
    ###open the file and remove all special symbols
    with open(input_text, "r", encoding='utf-8') as record:
        text_string = record.read()

    #lowercase if specified
    if "-I" in command_list:
        text_string = text_string.lower()

    ###split into a list of words (findall returns all occurences that match the pattern as a list of strings)
    word_list = re.findall("[a-zA-ZüöäÜÖÄß]+", text_string)
    
    ###count every distinct word and write into dictionary
    count_list = {}
    for word in word_list:
        if word in count_list:
            count_list[word]+=1
        else:
            count_list[word] = 1

    ###prints the sorted list
    if "-l" in command_list:
        count_list = sorted(count_list.items(), key=lambda x: (-x[1],x[0])) ### sort the list
        for key, value in count_list:
            print('%s\t%d' % (key, value))
            
    ###for testing purposes write the values into a text file
        """ test = open("test.txt", "w") 
        for key, value in count_list:
            test.write('%s\t%d\n' % (key, value)) 
        test.close()  """

    ###prints just the number of distinct words + all words
    else:
        print("%d/%d" % (len(count_list), len(word_list)))

if __name__ == "__main__":
    command_list = sys.argv
    input_text = command_list[-1]
    main()
    
