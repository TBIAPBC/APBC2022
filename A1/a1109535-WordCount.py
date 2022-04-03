import sys

ignore=False
list=False
file="unset"


def sort_dict_to_list(mydict):

    mylist=[]
    for entry in sorted(mydict.items(), key = lambda item:(-item[1],item[0]) ): #in my opinion wrong but true concerning the examples
    #for entry in sorted(mydict.items(), key = lambda item:(-item[1],item[0].lower()) ): #lower is necessary becaase otherwise it will sort all the uppercase and lowercase separated
        
        mylist.append(entry)
   
    return mylist


def word_count(str):
    
        #replace all numeric chars with blanks and join it
        str=''.join(content if content.isalnum() else " " for content in str)
        counts = dict()
        if ignore:
            str=(str.lower())


        words = str.split()
        

        #print the number of different words
        total_words=(len(words))#total word count
        different_words=total_words
        

        for word in words:
        
            if word in counts:
                counts[word] += 1
                different_words -=1
            else:
                counts[word] = 1

        #counts is my dictionary

        if list==False:
            print(different_words,"/",total_words)

        return counts



#this was my testtext
mytext="from hello HELLO Hello the?!otherside,it must abc abc dull dull dull have been--the~baby?!%$^()-_+Hase"



arguments = sys.argv[1:] #slicing the arguments
count = len(arguments)



#checking the parameters and setting the flags
if count>0:
    for x in range(1,count+1):
        if (sys.argv[x]=="-I"):
            ignore=True
        elif (sys.argv[x]=="-l"):
            list=True
        elif (x==count):
            #the file must always be the last argument
            file=sys.argv[x]


    with open(file,'r',encoding='utf-8') as content:
        mytext=content.read()
        content.close()

    

    output=( word_count(mytext))


    #nicht ganz richtiger print derzeit
    if list:
        for element in sort_dict_to_list(output):
            print("%s\t%s"%(element[0],element[1])) 
        

else:
    print("You need to insert at least 1 argument (the file to read)")

