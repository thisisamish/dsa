# Real-World Edge Cases and Quicksort Optimizations

> Practice Problems: [LC 215: Kth Largest Element](https://leetcode.com/problems/kth-largest-element-in-an-array/), [LC 973: K Closest Points to Origin](https://leetcode.com/problems/k-closest-points-to-origin/), [LC 347: Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/), [GFG: Median in Row-Wise Sorted Matrix](https://www.geeksforgeeks.org/dsa/find-median-row-wise-sorted-matrix/)

## Real-World Issues with Quicksort
### A. Worst-Case Time Complexity: O(n²)
- Happens if pivot always splits array poorly (e.g., already sorted input).
- **Solution**: Use randomized pivoting to avoid pathological cases.
```cpp
int randomizedPartition(vector<int>& arr, int low, int high) {
    int pivotIdx = low + rand() % (high - low + 1);
    swap(arr[pivotIdx], arr[high]); // randomize
    return lomutoPartition(arr, low, high);
}
```

### B. Tail Recursion / Stack Overflow
- Recursive calls can build up stack.
- **Solution**:
    - Use tail recursion optimization.
    - Always recurse into the smaller partition first.
```cpp
void optimizedQuicksort(vector<int>& arr, int low, int high) {
    while (low < high) {
        int pivot = lomutoPartition(arr, low, high);
        if (pivot - low < high - pivot) {
            optimizedQuicksort(arr, low, pivot - 1);
            low = pivot + 1;
        } else {
            optimizedQuicksort(arr, pivot + 1, high);
            high = pivot - 1;
        }
    }
}
```
    
## Advanced Interview Variants of Quickselect
### A. Find the Median of an Unsorted Array
- Use Quickselect with k = n/2.

### B. Find the k-th Smallest Distance Pair
- Use Quickselect with custom comparators.

### C. K-th Closest Points to Origin
- Use Quickselect with distance as the key.

## When to Use Quickselect vs Sorting
| Use Case                        | Use Quickselect? |
| ------------------------------- | ---------------- |
| Need exact order of all items   | ❌ No             |
| Need only k-th element          | ✅ Yes            |
| Need top-k or bottom-k elements | ✅ Sometimes      |
| Streaming data / online         | ❌ Use heaps      |

## Summary of Quicksort and Quickselect time complexities

| Algorithm       | Best Case  | Average Case | Worst Case |
| --------------- | ---------- | ------------ | ---------- |
| **Quicksort**   | $O(n log n)$ | $O(n log n)$   | $O(n²)$      |
| **Quickselect** | $O(n)$       | $O(n)$         | $O(n²)$      |
