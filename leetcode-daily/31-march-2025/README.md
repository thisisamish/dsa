# [2551. Put Marbles in Bags](https://leetcode.com/problems/put-marbles-in-bags/)

Date: March 31, 2025

Code available in: C++, Java, Python, Go

Difficulty: Medium

Tags: Greedy, Sorting

Pre-requisites: None

## Approach
The key insight is to note that if you split the marbles into contiguous segments (bags), then only the boundaries between segments add extra cost. Specifically, if you place a cut between positions `i` and `i + 1`, then you “pay” an extra cost of `weights[i] + weights[i + 1]`.

### Observation:

1. When all marbles are in one bag (`k = 1`), the cost is fixed as `weights[0] + weights[n – 1]` (first plus last marble).

2. For `k > 1`, every time you add a cut, you are “splitting” the bag into two, and the cost of the two resulting bags becomes:

    Left bag: `weights[start] + weights[i]`

    Right bag: `weights[i + 1] + weights[end]`

    Notice that aside from the fixed contributions from the very first and last marbles, each cut contributes an extra amount equal to `weights[i] + weights[i + 1]`.

3. No matter how you cut, the total cost always includes the fixed part: `weights[0] + weights[n – 1]`. The additional cost comes solely from the chosen `k – 1` cut boundaries. Therefore, the total score can be written as:
    $$ score = fixed + \sum_{\text{cut at i}}(weights[𝑖] + weights[i + 1])$$

4. To maximize the score, you would choose the `k – 1` cuts that have the largest contributions (largest values of `weights[i] + weights[i + 1]`).

    To minimize the score, you choose the `k – 1` cuts that have the smallest contributions.

## Code

## C++

Time Complexity: $O(n*logn)$

Space Complexity: $O(n)$

```cpp
class Solution {
public:
    long long putMarbles(vector<int>& weights, int k) {
        if (k == 1) return 0;

        int n = weights.size();
        vector<int> cut_contrib(n - 1, 0);

        for (int i = 0; i < n - 1; i++) {
            cut_contrib[i] = weights[i] + weights[i + 1];
        }
        sort(cut_contrib.begin(), cut_contrib.end());

        long long diff = 0;
        for (int i = 0; i < k - 1; i++) {
            diff += cut_contrib[n - 2 - i] - cut_contrib[i];
        }

        return diff;
    }
};
```

## Java

Time Complexity: $O(n*logn)$

Space Complexity: $O(n)$

```java
class Solution {
    public long putMarbles(int[] weights, int k) {
        if (k == 1) return 0;

        int n = weights.length;
        int[] cutContrib = new int[n - 1];

        for (int i = 0; i < n - 1; i++) {
            cutContrib[i] = weights[i] + weights[i + 1];
        }
        Arrays.sort(cutContrib);

        long diff = 0;
        for (int i = 0; i < k - 1; i++) {
            diff += cutContrib[n - 2 - i] - cutContrib[i];
        }

        return diff;
    }
}
```

## Python

Time Complexity: $O(n*logn)$

Space Complexity: $O(n)$

```py
class Solution:
    def putMarbles(self, weights: List[int], k: int) -> int:
        if k == 1:
            return 0

        n = len(weights)
        cut_contrib = sorted(weights[i] + weights[i + 1] for i in range(n - 1))

        return sum(cut_contrib[n - 2 - i] - cut_contrib[i] for i in range(k - 1))
```

## Go

Time Complexity: $O(n*logn)$

Space Complexity: $O(n)$

```go
func putMarbles(weights []int, k int) int64 {
    if k == 1 {
        return 0
    }

    n := len(weights)
    cutContrib := make([]int, n - 1)

    for i := range cutContrib {
        cutContrib[i] = weights[i] + weights[i + 1]
    }
    sort.Ints(cutContrib)

    var diff int64
    for i := 0; i < k - 1; i++ {
        diff += int64(cutContrib[n - 2 - i] - cutContrib[i])
    }

    return diff
}
```