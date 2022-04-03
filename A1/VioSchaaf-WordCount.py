import sys
import re

# read in file
filename = sys.argv[len(sys.argv)-1]
file = open(filename)


# check for options
list = False
ignore = False

for i in range(len(sys.argv)):
    if sys.argv[i] == "-l":
        list = True
    if sys.argv[i] == "-I":
        ignore = True


# create list of all words in the file

text = file.read()
regex = re.compile('[^a-zA-ZäöüÄÖÜß]', flags=re.UNICODE)

text = regex.sub(' ', text)
word_list = text.split()



# set to lower case if option "-I" is selected
if ignore:
    for i in range(len(word_list)):
        word_list[i] = word_list[i].lower()


# create list with all different words
different_words = []

for w1 in word_list:
    count = 0
    for w2 in different_words:
        if w1 == w2:
            break

    different_words.append(w1)


# if the option "-l" is selected, sort words by count
if list:
    count_list = []

    # count how often every word occurs
    for word in different_words:
        count = 0
        for word2 in word_list:
            if word == word2:
                count += 1

        count_list.append(count)

    # create dictionary with word as key and count as value
    dictionary = {}
    for i in range(0, len(different_words)):
        dictionary[different_words[i]] = count_list[i]

    # sort words by count number
    words_sorted = sorted(dictionary.items(), key=lambda x: (-x[1], x[0]))

    for i in words_sorted:
        print(i[0], "\t", i[1])


# print number of different words and number of total words if option "-l" is not selected
else:
    print(len(different_words), "/", len(word_list))
