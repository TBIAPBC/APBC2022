#include <iostream>
#include <string>
using namespace std;


int main(){
    
    cout << "Hello World!\n";
    
    string x;
    bool first{true};
    
    while(cin >> x){
        if (first){
            cout << x;
            first = false;
        }
        else 
            cout << " " << x;
    }
    
    return 0;
}

