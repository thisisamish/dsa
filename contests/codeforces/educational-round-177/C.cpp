#include <bits/stdc++.h>

using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        vector<int> p(n);
        unordered_map<int, int> m; // num : index
        for (int i = 0; i < n; i++) {
            int temp;
            cin >> temp;
            p[i] = temp;
            m[temp] = i;
        }
        for (int i = 0; i < n; i++) {
            int d;
            cin >> d;
            m[p[d - 1]] = -1;
            p[d - 1] = 0;
            while ()
        }
    }
    return 0;
}