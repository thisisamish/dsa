# [2873. Maximum Value of an Ordered Triplet I](https://leetcode.com/problems/maximum-value-of-an-ordered-triplet-i/)

Date: April 2, 2025

Code available in: C++

Difficulty: Trivial

Tags: Brute-force

Pre-requisites: None

## Approach
Since the constraints are very low, we can brute-force the solution. That makes this problem trivial. The more interesting solution is in the second part of this problem which has stricter constraints. Find that one [here](https://github.com/thisisamish/dsa/blob/main/leetcode-daily/03-april-2025/README.md).

## Code

## C++

Time Complexity: $O(n^3)$

Space Complexity: $O(1)$

```cpp
class Solution {
public:
    long long maximumTripletValue(vector<int>& nums) {
        long long ans = 0;
        int n = nums.size();
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                for (int k = j + 1; k < n; k++) {
                    long long  val = (nums[i] - nums[j]) * (long long) nums[k];
                    ans = val > 0 ? max(ans, val) : ans;
                }
            }
        }
        return ans;
    }
};
```