#include <iostream>
#include <fstream>
#include <string>
#include <random>
#include <vector>
#include <unordered_map>

using namespace std;


// random choose char from weighted distribution
const char choice(vector<char> bases, vector<double> weights, double num){
    bool cont = true;
    for (int i = 0; i < bases.size() - 1; i++){
        if (num < weights[i + 1] && num > weights[i]){
            return bases[i];
        }
    }
    return bases.back();
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

    // calc frequencies
    unordered_map<char, double> freq;
    for (auto c: input_content){
        freq[c] ++;
    }
    for (auto x: freq){
        freq[x.first] /= input_content.size();
    }

    // calc cumulative freq
    vector<char> bases;
    vector<double> weigths;
    double prev = 0.0;
    double h;
    for (auto x: freq){
        bases.push_back(x.first);
        prev = prev + x.second;
        weigths.push_back(prev);
    }

    // gen strings and save for possible further processing
    vector<string> out;
    uniform_real_distribution<double> distribution(0.0, 1.0);
    default_random_engine gen;

    for (int i = 0; i < n; i++) {
        string tmp;
        for (int j = 0; j < input_content.size(); j++) {
            double rand_double = distribution(gen);
            tmp += choice(bases, weigths, rand_double);
        }
        out.push_back(tmp);
    }

    // print solution
    for (auto s: out){
        cout << s << endl;
    }

    return 0;
}
