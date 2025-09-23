#include <bits/stdc++.h>

using namespace std;

int main() {
  int t;
  cin >> t;
  while (t--) {
    int n, k, x;
    cin >> n >> k >> x;
    vector<int> a(n * k);
    int i = 0;
    for (int j = 0; j < n; j++) {
      int temp;
      cin >> temp;
      int next_i = i + 1;
      for (int i = 0; i < k; i++) {
        a[i] = temp;
        i += n;
      }
      i = next_i;
    }
    vector<long long> prefix(n * k);
    vector<long long> suffix(n * k);
    prefix[0] = a[0];
    suffix[a.size() - 1] = a[a.size() - 1];
    for (int i = 1; i < a.size(); i++) {
        prefix[i] = prefix[i - 1] + a[i];
        suffix[a.size() - 1 - i] = suffix[a.size() - 2 - i] + a[a.size() - 1];
    }
    long long res = 0;
    for (int i = 0; i < a.size(); i++) {
        if (abs(prefix[i] - suffix[i]) >= 10) {
            res++;
        }
    }
    cout << res << "\n";
  }
  return 0;
}