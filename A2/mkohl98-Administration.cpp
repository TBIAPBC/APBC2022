#include <iostream>
#include <fstream>
#include <string>
#include <utility>
#include <vector>
#include <limits>
#include <map>
#include <list>
#include <algorithm>

using namespace std;


// init global variables
vector<pair<string, int>> solution;
int num_cities, limit;

// Node class
class Node{
    string name;  // id of node
    int cost;  // cost of node + parents
    int bound;  // upper bound
    vector<string> solution_path;  // contains solution
    vector<string> possible_children;  // children which could be appended
    Node* parent;  // pointer to parent node
    map<string, int> ref_node_costs;  //reference to get costs of current node
public:
    Node(string node_name, int node_cost, Node *node_parent, int &gbound, const map<string, int>& ref_node_costs,
         vector<string> parents_possible_children);
    void update_global_solution();
    void optimize_global_solution();
    bool check_cost() const;
    void update_cost();
    void update_possible_children(bool optimize);
    void update_solution_path();
    void solve(bool optimize);
};

Node::Node(string node_name, int node_cost, Node *node_parent, int &gbound, const map<string, int>& ref_node_costs,
           vector<string> parents_possible_children):
    name(move(node_name)),cost(node_cost), parent(node_parent), bound(gbound), ref_node_costs(ref_node_costs),
    possible_children(move(parents_possible_children)){
    if (this->parent == nullptr){
        this->solution_path.push_back(this->name);
    }
};

// append partial solution to global solution
void Node::update_global_solution() {
    pair<string, int> out;
    vector<string> vec_tmp = this->solution_path;
    list<string> list_tmp;
    vector<string> vec_sort_tmp;
    string path;

    // sort
    for (auto s: vec_tmp){
        list_tmp.push_back(s);
    };
    list_tmp.sort();
    for (auto s: list_tmp){
        vec_sort_tmp.push_back(s);
    }
    // merge to string
    for (int i = 0; i < vec_sort_tmp.size(); i++){
        if (i < vec_sort_tmp.size() - 1){
            path += vec_sort_tmp[i] + " ";
        } else {
            path += vec_sort_tmp[i];
        }
    }
    // check if already existing
    if (solution.empty()){
        out.first = path;
        out.second = this->cost;
        solution.push_back(out);
    } else {
        bool tmp_check = true;
        for (const auto& pair: solution) {
            if (pair.first == path) {
                tmp_check = false;
            }
        }
        if (tmp_check){
            out.first = path;
            out.second = this->cost;
            solution.push_back(out);
        }
    }
}

// lower upper bound and remove not optimal solutions
void Node::optimize_global_solution() {
    if (this->cost < limit){
        limit = this->cost;
    }
    vector<pair<string, int>> updated_solution;
    for (auto pair: solution){
        if (pair.second <= limit){
            updated_solution.push_back(pair);
        }
    }
    solution = updated_solution;
}

// check if node exceeds upper bound
bool Node::check_cost() const{
    return this->cost <= bound;
}

// update currents node costs by subracting parents costs - current nodes cost from cost map
void Node::update_cost() {
    if (this->parent != nullptr){
        this->cost = this->parent->cost + ref_node_costs[this->name];
    }
}

// update possible_children after adding new children
void Node::update_possible_children(bool optimize) {
    // filter possible children
    vector<string> new_possible_children;
    for (const auto &i : this->possible_children){
        if (i[0] != this->name[1] && i[0] != this->name[0] && i[1] != this->name[1] && i[1] != this->name[0]){
            new_possible_children.push_back(i);
        }
    }
    this->possible_children = new_possible_children;

    // update costs
    this->update_cost();

    // check if branch ends here
    if (this->possible_children.empty() && this->solution_path.size() == num_cities/2){
        if (this->check_cost()){
            this->update_global_solution();
            if (optimize){
                this->optimize_global_solution();
            }
        }
    }
}

// method to trace back solution
void Node::update_solution_path() {
    this->solution_path = this->parent->solution_path;
    this->solution_path.push_back(this->name);
}

// method to enumerate solutions less than fixed bound
void Node::solve(bool optimize) {
    while(!this->possible_children.empty() && this->check_cost()){
        string new_name = this->possible_children.back();
        this->possible_children.pop_back();

        Node child(new_name, ref_node_costs[new_name], this, bound, this->ref_node_costs, this->possible_children);
        child.update_solution_path();
        child.update_possible_children(optimize);
        child.solve(optimize);
    }
}

// function to split string into vector of strings
vector<string> split(string& str){
    vector<string> output;
    string word;
    bool skip = true;

    for (auto c: str){
        if (char(c) == ' '  && !skip){
            output.push_back(word);
            skip = true;
        } else if (char(c) != ' '  && skip){
            char append = c;
            word = append;
            skip = false;
        } else if (char(c) != ' '  && !skip){
            char append = c;
            word += append;
        }
    }
    output.push_back(word);
    return output;
}

vector<int> intify(vector<string> arr, int skip){
    vector<int> arr_out;
    int inf = numeric_limits<int>::max();

    for (int i = 0; i < arr.size(); i++){
        if (i == skip){
            arr_out.push_back(inf);
        } else {
            arr_out.push_back(stoi(arr[i]));
        }
    }
    return arr_out;
}

int main(int argc, char *argv[]) {
    // init
    bool opt = false;
    fstream input_file;

    // parse args
    if (argc == 1){
        cout << "Make sure to provide valid input file." << endl;
        return 0;
    }
    for (int i = 1; i < argc; i++){
        if (string(argv[i]) == "-o"){
            opt = true;
        } else {
            input_file.open(argv[i], ios::in);
        }
    }

    // check file
    if (!input_file) {
        cout << "Provided file is not existing." << endl;
        return 0;
    }

    // get file content
    string input_content, line;
    getline(input_file, line);
    vector<string> substrings = split(line);
    num_cities = stoi(substrings[0]);
    limit = stoi(substrings[1]);

    // get city names
    getline(input_file, line);
    vector<string> node_strings = split(line);

    // build adjacency matrix
    vector<vector<int>> adjacency_matrix;
    for (int i = 0; i < num_cities; i++){
        getline(input_file, line);
        adjacency_matrix.push_back(intify(split(line), i));
    }
    input_file.close();

    // assign costs to possible nodes for easy access
    map<string, int> node_costs;
    vector<string> node_names;
    for (int i = 0; i < num_cities; i++){
        for (int j = i + 1; j < num_cities; j++){
            string node_name = node_strings[i] + node_strings[j];
            node_costs[node_name] = adjacency_matrix[i][j];
            node_names.push_back(node_name);
        }
    }

    // solve
    for (const auto &root_name: node_names) {
        Node root(root_name, node_costs[root_name], nullptr, limit, node_costs, node_names);
        root.update_possible_children(opt);
        root.solve(opt);
    }

    // print solution
    for (const auto &x: solution) {
        cout << x.first << endl;
    }

    return 0;
}
