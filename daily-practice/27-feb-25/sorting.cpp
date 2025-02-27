#include <iostream>
#include <climits>

using namespace std;

void print_arr(int arr[], int size)
{
    for (int i = 0; i < size; i++)
    {
        cout << arr[i] << " ";
    }
    cout << "\n";
}

// TC: O(n^2) (worst/best/avg)
// SC: O(1) (in-place sorting)
// Stable: No
// No further optimisations can be done
void selection_sort(int arr[], int size)
{
    // Algorithm: Keep selecting the smallest element and putting it at the beginning
    // Iterate over the entire array except the last element because by the time we reach the last element, it will already be sorted
    for (int i = 0; i < size - 1; i++)
    {
        int minInd = i;
        for (int j = i + 1; j < size; j++)
        {
            if (arr[j] < arr[minInd])
            {
                minInd = j;
            }
        }
        // Swap if a new minimum has been found
        if (minInd != i)
        {
            int temp = arr[i];
            arr[i] = arr[minInd];
            arr[minInd] = temp;
        }
    }
}

// TC: Best - O(n), Avg - O(n^2), Worst - O(n^2)
// SC: O(1) (in-place sorting)
// Stable: Yes
void bubble_sort(int arr[], int size)
{
    // Algorithm: Keep swapping until the largest elements bubbles to the end of the array
    for (int i = 0; i < size - 1; i++)
    {
        bool swapped = false; // optimisation by checking if no swaps happened in a pass then the array is sorted
        for (int j = 1; j < size - i; j++)
        {
            if (arr[j] < arr[j - 1])
            {
                swapped = true;
                swap(arr[j], arr[j - 1]);
            }
        }
        if (!swapped)
        {
            break;
        }
    }
}

// TC: Best - O(n), Avg - O(n^2), Worst - O(n^2)
// SC: O(n) (stack space)
// Stable: Yes
// Algorithm: Keep swapping until the largest elements bubbles to the end of the array
void recursive_bubble_sort(int arr[], int end)
{
    if (end == 0)
    {
        return;
    }
    bool swapped = false; // optimisation by checking if no swaps happened in a pass then the array is sorted
    for (int j = 1; j <= end; j++)
    {
        if (arr[j] < arr[j - 1])
        {
            swapped = true;
            swap(arr[j], arr[j - 1]);
        }
    }
    if (!swapped)
    {
        return;
    }
    recursive_bubble_sort(arr, end - 1);
}

// TC: Worst/Avg - O(n^2); Best - O(n)
// SC: O(1) (in plac sorting)
// Stable: Yes
void insertion_sort(int arr[], int size)
{
    // Algorithm: Find an element's correct place and put it there
    for (int j = 1; j < size; j++)
    {
        if (arr[j] < arr[j - 1])
        {
            int k = j;
            while (k > 0 && arr[k] < arr[k - 1])
            {
                swap(arr[k], arr[k - 1]);
                k--;
            }
        }
    }
}

// TC: Worst/Avg - O(n^2); Best - O(n)
// SC: O(n) (stack space)
// Stable: Yes
// Algorithm: Find an element's correct place and put it there
void recursive_insertion_sort(int arr[], int size, int cur_size)
{
    if (cur_size >= size)
    {
        return;
    }
    if (arr[cur_size] < arr[cur_size - 1])
    {
        int k = cur_size;
        while (k > 0 && arr[k] < arr[k - 1])
        {
            swap(arr[k], arr[k - 1]);
            k--;
        }
    }
    recursive_insertion_sort(arr, size, cur_size + 1);
}

void merge(int arr[], int start, int mid, int end)
{
    int i = start;
    int j = mid + 1;
    int k = 0;
    int *sorted_arr = new int[end - start + 1];
    while (i <= mid && j <= end)
    {
        if (arr[i] <= arr[j])
        {
            sorted_arr[k] = arr[i];
            i++;
        }
        else
        {
            sorted_arr[k] = arr[j];
            j++;
        }
        k++;
    }
    while (i <= mid)
    {
        sorted_arr[k] = arr[i];
        i++;
        k++;
    }
    while (j <= end)
    {
        sorted_arr[k] = arr[j];
        j++;
        k++;
    }
    for (int i = start; i <= end; i++)
    {
        arr[i] = sorted_arr[i - start];
    }
    delete[] sorted_arr;
}

// TC: O(nlogn)
// SC: O(n)
// Stable: Yes
void merge_sort(int arr[], int start, int end)
{
    // Algorithm: Divide and conquer. Keep splitting into halves until one element is left and then keep merging.
    if (start != end)
    {
        int mid = start + (end - start) / 2;
        merge_sort(arr, start, mid);
        merge_sort(arr, mid + 1, end);
        merge(arr, start, mid, end);
    }
}

int main()
{
    int arr[] = {10, 9, 8, 7, 6, 5, 4, 3, 1};
    int size = sizeof(arr) / sizeof(arr[0]);
    cout << "Before sorting: " << endl;
    print_arr(arr, size);
    recursive_insertion_sort(arr, size, 1);
    cout << "After sorting: " << endl;
    print_arr(arr, size);
}