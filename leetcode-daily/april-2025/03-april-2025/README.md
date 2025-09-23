# [2873. Maximum Value of an Ordered Triplet II](https://leetcode.com/problems/maximum-value-of-an-ordered-triplet-ii/)

Date: April 3, 2025

Code available in: C++, Java, Python, Go

Difficulty: Medium

Tags: Greedy, Prefix Array, Suffix Array

Pre-requisites: None

## Approach 1: Greedy + Prefix and Suffix Arrays

1. We need to maximise $$(nums[i] - nums[j]) * nums[k]$$ where $i < j < k$.
2. For a given value of $nums[j]$, we will get the maximum value when $nums[i]$ and $nums[k]$ is maximum.
3. It is evident now that we can create a prefix array and a suffix array with $$prefix[i] = max(nums[0], nums[1],...nums[i])$$ and $$suffix[i] = max(nums[n - 1], nums[n - 2],...nums[i])$$
4. Now we can iterate over $nums$ and find out the max value of the triplet in $O(n)$ time.

## Approach 2: Greedy

1. Just like in approach 1 where we found out the max value for a given $nums[j]$, we we use $nums[k]$ here.
2. For a given $nums[k]$, the max value of $$(nums[i] - nums[j]) * nums[k]$$ where $i < j < k$ will be achieved when we have the max value of $$(nums[i] - nums[j])$$ which itself will be achieved when $nums[i]$ is maximum and $nums[j]$ is mimimum.

## Code

## C++

### Approach 1

Time Complexity: $O(n)$

Space Complexity: $O(n)$

```cpp
class Solution {
public:
    long long maximumTripletValue(vector<int>& nums) {
        int n = nums.size();

        // create prefix array
        vector<int> prefix(n);
        int lastMax = nums[0];
        for (int i = 0; i < n; i++) {
            lastMax = max(lastMax, nums[i]);
            prefix[i] = lastMax;
        }

        // create suffix array
        vector<int> suffix(n);
        lastMax = nums[n - 1];
        for (int i = n - 1; i >= 0; i--) {
            lastMax = max(lastMax, nums[i]);
            suffix[i] = lastMax;
        }

        // find max value of triplets
        long long maxVal = 0;
        for (int j = 1; j < n - 1; j++) {
            maxVal = max(maxVal, (prefix[j - 1] - nums[j]) * (long long)suffix[j + 1]);
        }

        return maxVal;
    }
};
```

### Approach 2

Time Complexity: $O(n)$

Space Complexity: $O(1)$

```cpp

```

## Java

### Approach 1

Time Complexity: $O(n)$

Space Complexity: $O(n)$

```java
class Solution {
    public long maximumTripletValue(int[] nums) {
        int n = nums.length;

        int[] prefix = new int[n];
        int lastMax = nums[0];
        for (int i = 0; i < n; i++) {
            lastMax = Math.max(lastMax, nums[i]);
            prefix[i] = lastMax;
        }

        int[] suffix = new int[n];
        lastMax = nums[n - 1];
        for (int i = n - 1; i >= 0; i--) {
            lastMax = Math.max(lastMax, nums[i]);
            suffix[i] = lastMax;
        }

        long maxVal = 0;
        for (int j = 1; j < n - 1; j++) {
            maxVal = Math.max(maxVal, (prefix[j - 1] - nums[j]) * (long)suffix[j + 1]);
        }

        return maxVal;
    }
}
```

### Approach 2

Time Complexity: $O(n)$

Space Complexity: $O(1)$

```java

```

## Python

### Approach 1

Time Complexity: $O(n)$

Space Complexity: $O(n)$

```py
class Solution:
    def maximumTripletValue(self, nums: List[int]) -> int:
        n = len(nums)

        prefix = [0] * n
        last_max = nums[0]
        for i in range(n):
            last_max = max(last_max, nums[i])
            prefix[i] = last_max

        suffix = [0] * n
        last_max = nums[-1]
        for i in range(n - 1, -1, -1):
            last_max = max(last_max, nums[i])
            suffix[i] = last_max

        max_val = 0
        for j in range(1, n - 1):
            max_val = max(max_val, (prefix[j - 1] - nums[j]) * suffix[j + 1])

        return max_val
        
```

### Approach 2

Time Complexity: $O(n)$

Space Complexity: $O(1)$

```py
class Solution:
    def maximumTripletValue(self, nums: List[int]) -> int:
        n = len(nums)
        res, imax, diffmax = 0, 0, 0
        for k in range(n):
            res = max(res, diffmax * nums[k])
            diffmax = max(diffmax, imax - nums[k])
            imax = max(imax, nums[k])
        return res
        
```

## Go

### Approach 1

Time Complexity: $O(n)$

Space Complexity: $O(n)$

```go
func maximumTripletValue(nums []int) int64 {
    n := len(nums)

    prefix := make([]int, n)
    lastMax := nums[0];
    for i := 0; i < n; i++ {
        lastMax = max(lastMax, nums[i]);
        prefix[i] = lastMax;
    }

    suffix := make([]int, n)
    lastMax = nums[n - 1];
    for i := n - 1; i >= 0; i-- {
        lastMax = max(lastMax, nums[i]);
        suffix[i] = lastMax;
    }

    var maxVal int64 = 0;
    for j := 1; j < n - 1; j++ {
        maxVal = max(maxVal, int64(prefix[j - 1] - nums[j]) * int64(suffix[j + 1]));
    }

    return maxVal;
}
```

### Approach 2

Time Complexity: $O(n)$

Space Complexity: $O(1)$

```go

```
