#include <iostream>
#include <climits>

using namespace std;

class Sorting
{
private:
    void printArr(int arr[], int size, const string &msg)
    {
        cout << msg;
        for (int i = 0; i < size; i++)
        {
            cout << arr[i] << " ";
        }
        cout << endl;
    }

public:
    Sorting() {}
    ~Sorting() {}

    // Time Complexity: Best/Avg/Worst - O(n + maxNum) where n is the size of array and maxNum is the biggest number in the array
    // Space Complexity: O(n + maxNum)
    // Stable: Yes
    void CountingSort(int arr[], int size)
    {
        printArr(arr, size, "Before sorting: ");

        // Find the biggest number
        int maxi = INT_MIN;
        for (int i = 0; i < size; i++)
        {
            maxi = max(maxi, arr[i]);
        }

        // Create and initialise the counting array
        int *counting = new int[maxi + 1]();

        // Fill the counting array
        for (int i = 0; i < size; i++)
        {
            counting[arr[i]]++;
        }

        // Create the cumulative count array
        for (int i = 1; i < maxi + 1; i++)
        {
            counting[i] += counting[i - 1];
        }

        // Create and fill the output array
        // Iterate backwards to preserve the stability
        int *output = new int[size];
        for (int i = size - 1; i >= 0; i--)
        {
            output[--counting[arr[i]]] = arr[i];
        }

        // Modify the input array with the sorted array
        for (int i = 0; i < size; i++)
        {
            arr[i] = output[i];
        }

        delete[] counting;
        delete[] output;

        printArr(arr, size, "After sorting: ");
    }

    // Time Complexity: Best/Avg/Worst - O(d(n + k)) where d is the number of digits in the maximum number in the array,
    // n is the size of array, and k = 10 for when all array elements are in decimal system
    // Space Complexity: O(n)
    // Stable: Yes
    void RadixSort(int arr[], int size)
    {
        printArr(arr, size, "Before sorting: ");

        // Find the biggest number
        int maxi = INT_MIN;
        for (int i = 0; i < size; i++)
        {
            maxi = max(maxi, arr[i]);
        }

        // Do counting sort on each digit starting from LSD
        int div = 1;
        while (maxi / div > 0)
        {
            int *count = new int[10]();
            int *lsd_arr = new int[size];
            // Create count and lsd arrays
            for (int i = 0; i < size; i++)
            {
                int lsd = (arr[i] / div) % 10;
                lsd_arr[i] = lsd;
                count[lsd]++;
            }
            // Make cumulative count array
            for (int i = 1; i < 10; i++)
            {
                count[i] += count[i - 1];
            }
            // Sort the array
            int *sorted = new int[size];
            for (int i = size - 1; i >= 0; i--)
            {
                int ind = lsd_arr[i];
                sorted[--count[ind]] = arr[i];
            }
            // Copy the sorted array into the original array
            for (int i = 0; i < size; i++)
            {
                arr[i] = sorted[i];
            }
            // Cleanup
            delete[] count;
            delete[] lsd_arr;
            delete[] sorted;
            div *= 10;
        }

        printArr(arr, size, "After sorting: ");
    }
};

int main()
{
    Sorting s = Sorting();
    int arr[] = {101, 4, 2, 2, 8, 3, 3, 1};
    s.RadixSort(arr, sizeof(arr) / sizeof(arr[0]));
    return 0;
}