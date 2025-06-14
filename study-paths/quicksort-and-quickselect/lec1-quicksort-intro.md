# Quicksort Intro

> Problems to solve: [LC 912. Sort an Array](https://leetcode.com/problems/sort-an-array/)

## What is Quicksort?
- Quicksort is a <u>divide-and-conquer</u> sorting algorithm invented by Tony Hoare in 1959.
- Despite its worst-case time complexity being O(n²), it is one of the fastest and most widely used sorting algorithms in practice, especially with good pivot selection and randomization.
- It is <u>unstable</u> due to random swapping of elements in its operation.
- It sorts <u>in-place</u>.

## High Level Idea
1. Choose a pivot element from the array.
2. Partition the array into:
    - Elements less than the pivot
    - The pivot itself
    - Elements greater than the pivot
3. Recursively apply the same strategy to the left and right subarrays.

## Why Quicksort Works
It reduces the problem size with each recursive call:
- After each partition, the pivot is at its correct final position.
- The subarrays are independent and can be sorted separately.

## Time and Space Complexity
- Best Case TC - $O(n log n)$ [Balanced partitioning (e.g., always pick median)]
- Average Case TC - $O(n log n)$ [Random or well-distributed pivots]
- Worst Case TC - $O(n^2)$ [Poor pivots (e.g., already sorted array + bad pivot choice)]
- SC - $O(log n)$ [Due to recursion stack (in-place otherwise)]

## Key Concept - Partitioning
Partitioning is the core step where:
* We pick a pivot.
* We rearrange the array such that:
    - All elements less than pivot come before it.
    - All elements greater than pivot come after it.

There are two main partitioning schemes:
1. Lomuto Partition Scheme (simpler, single pointer)
2. Hoare Partition Scheme (more efficient, dual pointer)

## When NOT To Use Quicksort
- If worst-case performance must be avoided (e.g., time-sensitive systems).
- If stability is required (Quicksort is not stable by default).
- If sorting linked lists – MergeSort is better.

## How It Is Used In Practice
- Python’s .sort() and Java’s Arrays.sort() use Timsort (a hybrid of MergeSort + InsertionSort).
- C++ STL std::sort uses Introsort, which starts with Quicksort and switches to Heapsort when recursion depth gets too high.

## Quicksort Algorithm (Lomuto Partition)
1. Main function: `QuickSort(arr, low, high)`

    Algorithm QuickSort(arr, low, high):
    
        1. If low is less than high, do the following:
            a. Partition the array around a pivot and get the pivot index.
            b. Recursively apply QuickSort on the left sub-array (from low to pivot index - 1).
            c. Recursively apply QuickSort on the right sub-array (from pivot index + 1 to high).
2. Helper Function: `Partition(arr, low, high)`

    Algorithm Partition(arr, low, high):

        1. Choose the last element of the array (arr[high]) as the pivot.
        2. Initialize a pointer i to (low - 1) — this marks the position for swapping.
        3. For each element from index low to (high - 1):
            a. If the current element is less than the pivot:
                i. Increment i.
                ii. Swap arr[i] with the current element (arr[j]).
        4. After the loop, swap the element at (i + 1) with the pivot (arr[high]).
        5. Return the index (i + 1) as the pivot index.

## Quicksort (Lomuto Partition) Implementation in C++
```cpp
class Solution {
void quicksort(vector<int>& nums, int low, int high) {
    if (low < high) {
        int pivot_ind = partition(nums, low, high);
        quicksort(nums, low, pivot_ind - 1);
        quicksort(nums, pivot_ind + 1, high);
    }
}

int partition(vector<int>& nums, int low, int high) {
    int pivot = nums[high];
    int i = low - 1;

    for (int j = low; j < high; j++) {
        if (nums[j] < pivot) {
            i++;
            swap(nums[i], nums[j]);
        }
    }
    swap(nums[i + 1], nums[high]);

    return i + 1;
}

public:
    vector<int> sortArray(vector<int>& nums) {
        int n = nums.size();
        quicksort(nums, 0, n - 1);
        return nums;
    }
};
```

