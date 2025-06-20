# Frequently Asked Quicksort and Quickselect Interview Problems

## Problem 1: Kth Largest Element in an Array
[LeetCode 215](https://leetcode.com/problems/kth-largest-element-in-an-array/): Given an array nums, find the kth largest element.
- **Insight**: Use Quickselect to find the n - k smallest element.
- **Time**: $O(n)$ average, $O(n²)$ worst (mitigated by random pivoting)

## Problem 2: K Closest Points to Origin
[LeetCode 973](https://leetcode.com/problems/k-closest-points-to-origin/): Given a list of points on a plane, return the k closest points to the origin (0, 0).
- **Insight**: Use Quickselect with custom comparator (distance² = x² + y²).
- Use Quickselect to partition until kth smallest distance is found.

## Problem 3: Kth Smallest Element in a Sorted Matrix
[LeetCode 378](https://leetcode.com/problems/kth-smallest-element-in-a-sorted-matrix/): Given an n x n matrix where each row and column is sorted, find the kth smallest element.
- **Insight**: This is not a pure Quickselect problem.
- Use binary search over value range or a min-heap.
- Explain why Quickselect is not ideal here, even though the problem asks for the "kth smallest".

## Problem 4: Top K Frequent Elements
[LeetCode 347](https://leetcode.com/problems/top-k-frequent-elements/): Given an array of integers, return the k most frequent elements.
- **Insight**: Count frequencies → apply Quickselect on the counts.
- Partition based on frequency instead of value.
- Explain how to use Quickselect here instead of a heap. What is the pivot in this context?

## Problem 5: Sort Colors / Dutch National Flag
[LeetCode 75](https://leetcode.com/problems/sort-colors/): Sort an array containing only 0s, 1s, and 2s in-place.
- **Insight**: Variant of 3-way QuickSort partitioning (Dijkstra’s algorithm).
- **Time**: $O(n)$, in-place, one pass
- Explain the connection to Quicksort and why this works in linear time.