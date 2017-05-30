#include <iostream>
#include <algorithm>
#include <string>
#include <vector>
#include <cmath>
#include <random>
using namespace std;

random_device rd;
mt19937	mt(rd());
uniform_int_distribution<int> sou(0,11);
uniform_int_distribution<int> flag(0,10000);
vector<int> ground(5,0);
vector<int> oto(5,0);

int n;
int k;
int main(){
	cin >> n;
	for(int i=0;i<n;i++){
		for(int j=0;j<5;j++){
			if(ground[j]==0){
				oto[j] = sou(mt);
				k = flag(mt);
				if(k<3000){
					ground[j] = 1;
				}
			}else{
				k = flag(mt);
				if(k>=9000){
					ground[j] = 0;
				}
			}
		}
		for(int j=0;j<5;j++){
			cout << oto[j] << " ";
		}
		for(int j=0;j<4;j++){
			cout << ground[j] << " ";
		}
		cout << ground[4] << endl;
	}
}