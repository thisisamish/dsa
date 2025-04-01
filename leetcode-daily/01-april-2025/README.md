# [2140. Solving Questions With Brainpower](https://leetcode.com/problems/solving-questions-with-brainpower)

Date: April 1, 2025

Code available in: C++, Java, Python, Go

Difficulty: Easy

Tags: Dynamic Programming, 1D Dynamic Programming, Knapsack, 0/1 Knapsack

Pre-requisites: 0/1 Knapsack Dynamic Programming

> Note: The language specific code files in this folder have only the most efficient solution.

## Approach
Classic pick/don't pick dp format. No hidden pitfalls to be aware of.

## Code

## C++

### Top-down/Recursive Approach
Time Complexity: $O(2^n)$

Space Complexity: $O(n)$

```cpp
class Solution {
public:
    long long recurse(int i, vector<vector<int>>& questions) {
        int n = questions.size();
        if (i >= n) return 0;

        long long solve = questions[i][0] + recurse(i + 1 + questions[i][1], questions);
        long long skip = recurse(i + 1, questions);

        return max(solve, skip);
    }
    long long mostPoints(vector<vector<int>>& questions) {
        return recurse(0, questions);
    }
};
```

### Top-down/Recursive Approach (with memoization)
Time Complexity: $O(n)$

Space Complexity: $O(n)$

```cpp
class Solution {
public:
    long long recurse(int i, vector<vector<int>>& questions, vector<long long>& dp) {
        int n = questions.size();
        if (i >= n) return 0;
        if (dp[i] != -1) return dp[i];

        long long solve = questions[i][0] + recurse(i + 1 + questions[i][1], questions, dp);
        long long skip = recurse(i + 1, questions, dp);

        return dp[i] = max(solve, skip);
    }
    long long mostPoints(vector<vector<int>>& questions) {
        int n = questions.size();
        vector<long long> dp(n, -1);
        return recurse(0, questions, dp);
    }
};
```

### Bottom-up Approach
Time Complexity: $O(n)$

Space Complexity: $O(n)$

```cpp
class Solution {
public:
    long long mostPoints(vector<vector<int>>& questions) {
        int n = questions.size();
        vector<long long> dp(n, -1);
        dp[n - 1] = questions[n - 1][0];

        for (int i = n - 2; i >= 0; i--) {
            int nextIndex = i + questions[i][1] + 1;
            long long solve = questions[i][0] + (nextIndex < n ? dp[nextIndex] : 0);
            dp[i] = max(solve, dp[i + 1]);
        }

        return dp[0];
    }
};
```

## Java

### Top-down/Recursive Approach
Time Complexity: $O(2^n)$

Space Complexity: $O(n)$

```java
class Solution {
    public long recurse(int i, int[][] questions) {
        int n = questions.length;
        if (i >= n) return 0;

        long solve = questions[i][0] + recurse(i + 1 + questions[i][1], questions);
        long skip = recurse(i + 1, questions);

        return Math.max(solve, skip);
    }

    public long mostPoints(int[][] questions) {
        return recurse(0, questions);    
    }
}
```

### Top-down/Recursive Approach (with memoization)
Time Complexity: $O(n)$

Space Complexity: $O(n)$

```java
class Solution {
    public long recurse(int i, int[][] questions, long[] dp) {
        int n = questions.length;
        if (i >= n) return 0;
        if (dp[i] != -1) return dp[i];

        long solve = questions[i][0] + recurse(i + 1 + questions[i][1], questions, dp);
        long skip = recurse(i + 1, questions, dp);

        return dp[i] = Math.max(solve, skip);
    }

    public long mostPoints(int[][] questions) {
        int n = questions.length;
        long[] dp = new long[n];
        Arrays.fill(dp, -1);
        return recurse(0, questions, dp);    
    }
}
```

### Bottom-up Approach
Time Complexity: $O(n)$

Space Complexity: $O(n)$

```java
class Solution {
    public long mostPoints(int[][] questions) {
        int n = questions.length;
        long[] dp = new long[n];
        dp[n - 1] = questions[n - 1][0];

        for (int i = n - 2; i >= 0; i--) {
            int nextIndex = i + questions[i][1] + 1;
            long solve = questions[i][0] + (nextIndex < n ? dp[nextIndex] : 0);
            dp[i] = Math.max(solve, dp[i + 1]);
        }

        return dp[0];
    }
}
```

## Python

### Top-down/Recursive Approach
Time Complexity: $O(2^n)$

Space Complexity: $O(n)$

```py
class Solution:
    def mostPoints(self, questions: List[List[int]]) -> int:
        n = len(questions)

        def recurse(i):
            if i >= n:
                return 0
            
            solve = questions[i][0] + recurse(i + 1 + questions[i][1])
            skip = recurse(i + 1)

            return max(solve, skip)
        
        return recurse(0)
```

### Top-down/Recursive Approach (with memoization)
Time Complexity: $O(n)$

Space Complexity: $O(n)$

```py
class Solution:
    def mostPoints(self, questions: List[List[int]]) -> int:
        n = len(questions)
        dp = [-1] * n
        
        def recurse(i):
            if i >= n:
                return 0
            if dp[i] != -1:
                return dp[i]
            
            solve = questions[i][0] + recurse(i + 1 + questions[i][1])
            skip = recurse(i + 1)

            dp[i] = max(solve, skip)
            return dp[i]
        
        return recurse(0)
```

### Bottom-up Approach
Time Complexity: $O(n)$

Space Complexity: $O(n)$

```py
class Solution:
    def mostPoints(self, questions: List[List[int]]) -> int:
        n = len(questions)
        dp = [-1] * n
        dp[n - 1] = questions[n - 1][0]

        for i in range(n - 2, -1, -1):
            next_index = i + questions[i][1] + 1
            solve = questions[i][0] + (dp[next_index] if next_index < n else 0)
            dp[i] = max(solve, dp[i + 1])

        return dp[0]
```

## Go

### Top-down/Recursive Approach
Time Complexity: $O(2^n)$

Space Complexity: $O(n)$

```go
func mostPoints(questions [][]int) int64 {
    n := len(questions)

    var recurse func(int) int64
    recurse = func(i int) int64 {
        if i >= n {
            return 0
        }

        solve := int64(questions[i][0]) + recurse(i + 1 + questions[i][1])
        skip := recurse(i + 1)

        return max(solve, skip)
    }

    return recurse(0)
}
```

### Top-down/Recursive Approach (with memoization)
Time Complexity: $O(n)$

Space Complexity: $O(n)$

```go
func mostPoints(questions [][]int) int64 {
    n := len(questions)
    dp := make([]int64, n)
    for i := range dp {
        dp[i] = -1
    }

    var recurse func(int) int64
    recurse = func(i int) int64 {
        if i >= n {
            return 0
        }
        if dp[i] != -1 {
            return dp[i]
        }

        solve := int64(questions[i][0]) + recurse(i + 1 + questions[i][1])
        skip := recurse(i + 1)

        dp[i] = max(solve, skip)
        return dp[i]
    }

    return recurse(0)
}
```

### Bottom-up Approach
Time Complexity: $O(n)$

Space Complexity: $O(n)$

```go
func mostPoints(questions [][]int) int64 {
    n := len(questions)
    dp := make([]int64, n)
    for i := range dp {
        dp[i] = -1
    }
    dp[n - 1] = int64(questions[n - 1][0])

    for i := n - 2; i >= 0; i-- {
        nextIndex := i + questions[i][1] + 1
        solve := int64(questions[i][0]) 
        if nextIndex < n {
            solve += dp[nextIndex]
        }
        dp[i] = max(solve, dp[i + 1])
    }

    return dp[0]
}
```