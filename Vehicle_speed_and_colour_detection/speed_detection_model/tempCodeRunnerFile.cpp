#include<iostream>
using namespace std;

int main(){
    int n;
    cin >> n;
    string w;
    while(n--){
        cin >> w;
        long len;
        len = w.size();
        if (len > 10){
            cout << w[0] << len << w[len-1] << endl;
        }
        else{
            cout << w << endl;
        }
    }
}