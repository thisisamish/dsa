# Advanced Optimizations, Custom Comparators, and Real-World Applications of Quickselect & Quicksort

## Part 1: Handling Duplicates & Skewed Data

> Problems to solve: [LC 215: Kth largest with repeated values](https://leetcode.com/problems/kth-largest-element-in-an-array/), [LC 280: Wiggle Sort](https://www.lintcode.com/problem/508/)

### Problem: Why is standard Quicksort inefficient with many duplicates?
Imagine an array like [1, 1, 1, 1, 2, 3].
- If we always split into `<` pivot and `>=` pivot, what happens?
- We’ll keep partitioning almost the entire array of 1s, gaining no performance benefit.

### Solution: 3-Way Partitioning (Dutch National Flag style)
This splits the array into:
- `<` pivot
- `==` pivot
- `>` pivot

Time: $O(n)$

Useful when:
- Array has many duplicates
- Need to group values, not just sort

### Bonus: Wiggle Sort
Given: `[1, 5, 1, 1, 6, 4]`

Output: `[1, 6, 1, 5, 1, 4]` such that `nums[0] < nums[1] > nums[2] < nums[3]...`

Approach:
1. Find median using Quickselect
2. Three-way partition the array around median
3. Virtual index mapping trick for correct placement

## Part 2: Quickselect with Custom Comparators

> Problems to solve: [LC 692: K Most Frequent Words](https://leetcode.com/problems/top-k-frequent-words/), [LC 658: K Closest Elements](https://leetcode.com/problems/find-k-closest-elements/)

## Part 3: Introsort — Real-World Optimization
### Why Introsort?
- Quicksort is great on average but has O(n²) worst-case
- C++ STL (`std::sort`) uses Introsort — a hybrid of:
    - Quicksort (fast)
    - Heapsort (for deep recursions)
    - Insertion sort (for small ranges)
### How it works:
- Start with Quicksort.
- If recursion depth > $2×log₂(n)$, switch to Heapsort.
- If subarray size < 16, use Insertion sort.

