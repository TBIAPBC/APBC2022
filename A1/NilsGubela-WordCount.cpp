#include <iostream>
#include <fstream>
#include <string>
#include <stdio.h>
#include <map>
#include <boost/range/numeric.hpp>
#include <boost/range/adaptor/map.hpp>
using namespace std;


int main(int argc, char **argv)
{
  // initialize flag arguments
  bool ignore = false;
  bool list = false;
  int index_dataname = 1;
  string file_name;

  // read in flag arguments from command line
  int i = 1;
  while (i < argc){
    if (strcmp( argv[i], "-I") == 0){
      ignore = true;
      i += 1;
    } else if(strcmp( argv[i], "-l") == 0){
      list = true;
      i += 1;
    }else {
      index_dataname = i;
      file_name = argv[index_dataname];
      i += 1;
    }
  }

  // initialize world list as associative array
  std::map <string, int> word_list;

  // read in file
  fstream file;
  file.open(file_name.c_str());

  // extracting words from the file
  string word;
  while (file >> word)
    {   
      // displaying content
      int i = 0;
      string word1 = "";
      while(i < word.length()){
        if((word[i]>='a' && word[i]<='z') || (word[i]>='A' && word[i]<='Z')) {
          if(ignore){
            word1 += tolower(word[i]);  
          }else{
            word1 += word[i];
          }
          i += 1;
        }else{
          // save word1 to list
          if(word1.length() > 0){
            if (word_list.find(word1) == word_list.end()) {
               word_list[word1] = 1;
            } else {
               word_list[word1] += 1;
            }
          }
          //start new word
          word1 = "";
          i += 1;
        }
      }
      if(word1.length() > 0){
        if (word_list.find(word1) == word_list.end()) {
             word_list[word1] = 1;
          } else {
             word_list[word1] += 1;
          }
      }

    }

if(list){
  map<string, int>::iterator it;
  int n = word_list.size();
  string names[n];
  int values[n];
  string tmp_string;
  int tmp_int;
  int index = 0;

  for (it = word_list.begin(); it != word_list.end(); it++)
  {
    names[index] = it->first;
    values[index] = it->second;
    index+=1;

  }



 for (int j = n-2; j >0; j--)
  {
    for (int k = 0; k < j; k++)
    {
      if (values[k] < values[k+1])
      {

        tmp_int = values[k];
        values[k] = values[k+1];
        values[k+1] = tmp_int;

        tmp_string = names[k];
        names[k] = names[k+1];
        names[k+1] = tmp_string;        
      }
    }
  }

  for (int j = 0; j < n; j++)
  {
  std::cout << names[j]   // string (key)
            << '\t'
            << values[j]   // string's value 
            << std::endl;

  }

}else{
  int words = word_list.size();
  int total_sum = boost::accumulate(word_list | boost::adaptors::map_values, 0);


  printf("%d / %d \n", words, total_sum);
}
  return 0;
 }
