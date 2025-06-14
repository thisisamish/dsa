## Lomuto And Hoare Partitioning

> Problems to solve: [LC 912. Sort an Array](https://leetcode.com/problems/sort-an-array/)

## 1. Lomuto Partitioning

### Idea:
- Always picks the last element as pivot
- Uses a single pointer to track the partition boundary

### Pros:
- Simple to implement
- Works well for educational purposes

### Cons:
- Performs more swaps than necessary
- Performs worse on arrays with many duplicates

### C++ Implementation:
```cpp
int lomutoPartition(vector<int>& arr, int low, int high) {
    int pivot = arr[high];
    int i = low - 1;

    for (int j = low; j < high; ++j) {
        if (arr[j] < pivot) {
            ++i;
            swap(arr[i], arr[j]);
        }
    }
    swap(arr[i + 1], arr[high]);
    return i + 1;
}
```

## 2. Hoare Partition

### Idea:
- Picks the first element as pivot (can be randomized)
- Uses two pointers that move toward each other

### Pros:
- Fewer swaps, more efficient in practice
- Better for arrays with duplicates

### Cons:
- Doesn’t place pivot in its final sorted position
- Slightly harder to implement correctly

### C++ Implementation:
```cpp
int hoarePartition(vector<int>& arr, int low, int high) {
    int pivot = arr[low];
    int i = low - 1;
    int j = high + 1;

    while (true) {
        do { i++; } while (arr[i] < pivot);
        do { j--; } while (arr[j] > pivot);

        if (i >= j) return j;

        swap(arr[i], arr[j]);
    }
}
```

> **! Important Note**: When using Hoare's partition in Quicksort:
```cpp
quicksort(arr, low, p);        // Not p - 1
quicksort(arr, p + 1, high);   // Because pivot is not necessarily at position `p`
```

## C++ Implementation of Quicksort with Hoare's Partition
```cpp
class Solution {
void quicksort(vector<int>& nums, int low, int high) {
    if (low < high) {
        int pivot_ind = partition(nums, low, high);
        quicksort(nums, low, pivot_ind);
        quicksort(nums, pivot_ind + 1, high);
    }
}

int partition(vector<int>& nums, int low, int high) {
    int pivot = nums[low];
    int i = low - 1;
    int j = high + 1;

    while (true) {
        do { i++; } while (nums[i] < pivot);
        do { j--; } while (nums[j] > pivot);

        if (i >= j) return j;

        swap(nums[i], nums[j]);
    }
}

public:
    vector<int> sortArray(vector<int>& nums) {
        int n = nums.size();
        quicksort(nums, 0, n - 1);
        return nums;
    }
};
```