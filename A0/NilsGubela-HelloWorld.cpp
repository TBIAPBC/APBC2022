#include <iostream>
#include <fstream>
#include <string>
using namespace std;

int main (int argc, char *argv[]) 
{
  cout<<"Hello World!"<<endl;  
  ifstream myfile(argv[1]);

  string line;
   while( getline( myfile, line ) ) {
       cout << line <<endl;
   }
  return 0;
}