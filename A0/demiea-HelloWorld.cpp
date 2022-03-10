#include<iostream>
#include<fstream>

using namespace std;

int main() {
// create a string

string file_name;
//first output
  cout << "Hello Wolrd! \n";
//get file via command line and save contend into string
  getline(cin, file_name);
//output string
   cout << file_name;


  return 0;
};
