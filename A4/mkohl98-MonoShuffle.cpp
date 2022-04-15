#include <iostream>
#include <fstream>
#include <string>
#include <random>
#include <vector>

using namespace std;


void swap(string &str, int i, int j){
    char h = str[i];
    str[i] = str[j];
    str[j] = h;
}


int main(int argc, char *argv[]) {
    // init args
    fstream input_file;
    int n = 3;

    // parse args
    if (argc == 1){
        cout << "Make sure to provide valid input file." << endl;
        return 0;
    }
    for (int i = 1; i < argc; i++){
        if (string(argv[i]) == "-N"){
            n = stoi(argv[i+1]);
        } else {
            input_file.open(argv[i], ios::in);
        }
    }

    // check file
    if (!input_file) {
        cout << "Provided file does not exist." << endl;
        return 0;
    }

    // get file content
    string input_content;
    getline(input_file, input_content);
    input_file.close();


    // gen strings and save for possible further processing
    vector<string> out;
    default_random_engine gen;
    int len = input_content.size();

    for (int i = 0; i < n - 1; i++) {
        string tmp = input_content;
        for (int j = 0; j < len; j++) {
            uniform_int_distribution<int> distribution(j, len - 1);
            int rand_int = distribution(gen);
            swap(tmp, j, rand_int);
        }
        out.push_back(tmp);
    }

    // print solution
    for (auto s: out){
        cout << s << endl;
    }

    return 0;
}
