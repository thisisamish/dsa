# LeetCode #1: [Two Sum](https://leetcode.com/problems/two-sum/description/)

## Problem Description
Given an array of integers nums and an integer target, return the indices of the two numbers in the array that add up to the target.

You may assume that each input has exactly one solution, you cannot use the same element twice, and you can return the answer in any order.

## Approaches

### 1. Naive Approach: Brute Force
The most straightforward way is to check all possible pairs of numbers in the array.

#### Algorithm
Use two nested loops to iterate through each pair of elements.
For each pair, check if they sum to the target.
Return the indices when a match is found.

#### Complexity Analysis

**Time Complexity:** *O(n²)*

**Space Complexity:** *O(1)*

### 2. Optimized Approach: Hash Map (One-pass)
We can use a hash map to track values we've seen and find complements efficiently.

#### Algorithm

Create an empty hash map to store numbers and their indices.
Iterate through the array once.
For each element, calculate its complement (target - current value).
If the complement exists in our hash map, return the current index and the complement's index.
Otherwise, add the current element and its index to the hash map.
Continue the iteration.

#### Complexity Analysis

**Time Complexity:** *O(n)*
**Space Complexity:** *O(n)*

## Alternative Approaches (Less Common)

### Two-Pointer Approach (Requires Sorting)

Sort the array (keeping track of original indices).
Use two pointers (left and right) to find the pair.

**Time Complexity:** *O(n log n)* due to sorting

### Binary Search (Requires Sorting)

Sort the array (keeping track of original indices).
For each element, binary search for its complement.

**Time Complexity:** *O(n log n)* due to sorting

## C++ Solutions

### Solution 1: Brute Force
```cpp
class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        int n = nums.size();
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                if (nums[i] + nums[j] == target) {
                    return {i, j};
                }
            }
        }
        // No solution found (though problem guarantees one exists)
        return {}; 
    }
};
```

### Solution 2: Hash Map (One-pass)
```cpp
class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        unordered_map<int, int> numMap; // value -> index
        
        for (int i = 0; i < nums.size(); i++) {
            int complement = target - nums[i];
            
            // Check if the complement exists in the map
            if (numMap.find(complement) != numMap.end()) {
                return {numMap[complement], i};
            }
            
            // Add current number to the map
            numMap[nums[i]] = i;
        }
        
        // No solution found (though problem guarantees one exists)
        return {};
    }
};
```

## Python Solutions

### Solution 1: Brute Force
```python
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        n = len(nums)
        for i in range(n):
            for j in range(i + 1, n):
                if nums[i] + nums[j] == target:
                    return [i, j]
        # No solution found (though problem guarantees one exists)
        return []
```

### Solution 2: Hash Map (One-pass)
```python
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        num_map = {}  # value -> index
        
        for i, num in enumerate(nums):
            complement = target - num
            
            # Check if the complement exists in the map
            if complement in num_map:
                return [num_map[complement], i]
            
            # Add current number to the map
            num_map[num] = i
        
        # No solution found (though problem guarantees one exists)
        return []
```

## Java Solutions

### Solution 1: Brute Force
```java
class Solution {
    public int[] twoSum(int[] nums, int target) {
        int n = nums.length;
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                if (nums[i] + nums[j] == target) {
                    return new int[] {i, j};
                }
            }
        }
        // No solution found (though problem guarantees one exists)
        return new int[] {};
    }
}
```

### Solution 2: Hash Map (One-pass)
```java
class Solution {
    public int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> numMap = new HashMap<>(); // value -> index
        
        for (int i = 0; i < nums.length; i++) {
            int complement = target - nums[i];
            
            // Check if the complement exists in the map
            if (numMap.containsKey(complement)) {
                return new int[] {numMap.get(complement), i};
            }
            
            // Add current number to the map
            numMap.put(nums[i], i);
        }
        
        // No solution found (though problem guarantees one exists)
        return new int[] {};
    }
}
```

## Go Solutions

### Solution 1: Brute Force
```go
func twoSum(nums []int, target int) []int {
    n := len(nums)
    for i := 0; i < n; i++ {
        for j := i + 1; j < n; j++ {
            if nums[i] + nums[j] == target {
                return []int{i, j}
            }
        }
    }
    // No solution found (though problem guarantees one exists)
    return []int{}
}
```

### Solution 2: Hash Map (One-pass)
```go
func twoSum(nums []int, target int) []int {
    numMap := make(map[int]int) // value -> index
    
    for i, num := range nums {
        complement := target - num
        
        // Check if the complement exists in the map
        if idx, found := numMap[complement]; found {
            return []int{idx, i}
        }
        
        // Add current number to the map
        numMap[num] = i
    }
    
    // No solution found (though problem guarantees one exists)
    return []int{}
}
```