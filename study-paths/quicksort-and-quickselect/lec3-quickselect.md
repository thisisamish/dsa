# Quickselect

> Practice Problems: [LC 215. Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/), [LC 973. K Closest Points to Origin](https://leetcode.com/problems/k-closest-points-to-origin/)

## What is Quickselect?
- Quickselect is an efficient selection algorithm to find the k-th smallest (or largest) element in an unsorted array.
- It’s related to Quicksort, using the same partitioning approach.
- Average time complexity: $O(n)$ — faster than sorting the whole array $O(n log n)$.

## Why Quickselect?
- Useful in interviews for problems like:
    - Find the median.
    - Find k-th smallest/largest element.
    - Solve order-statistics queries efficiently.
    
## How Quickselect Works
- Pick a pivot (e.g., last element).
- Partition the array.
- Let `pivotIndex` be the position where pivot lands after partition.
- Compare `pivotIndex` with `k`:
    - If `pivotIndex == k`, pivot is the k-th smallest element → return it.
    - If `pivotIndex > k`, recurse on left subarray.
    - If `pivotIndex < k`, recurse on right subarray (adjusting k accordingly).

## Time And Space Complexity:
- Average Case TC - $O(n)$
- Worst Case TC - $O(n^2)$ (bad pivots)
- SC - $O(log n)$

## Quickselect Implementation (using Lomuto partition) in C++
```cpp
int lomutoPartition(vector<int>& arr, int low, int high) {
    int pivot = arr[high];
    int i = low - 1;
    for (int j = low; j < high; ++j) {
        if (arr[j] <= pivot) {
            i++;
            swap(arr[i], arr[j]);
        }
    }
    swap(arr[i + 1], arr[high]);
    return i + 1;
}

int quickselect(vector<int>& arr, int low, int high, int k) {
    if (low == high) // Only one element
        return arr[low];

    int pivotIndex = lomutoPartition(arr, low, high);

    if (pivotIndex == k)
        return arr[pivotIndex];
    else if (pivotIndex > k)
        return quickselect(arr, low, pivotIndex - 1, k);
    else
        return quickselect(arr, pivotIndex + 1, high, k);
}
```