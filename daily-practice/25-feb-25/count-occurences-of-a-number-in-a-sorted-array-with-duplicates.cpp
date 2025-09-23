// PS: Given a sorted array, arr[] and a number target, you need to find the number of occurrences of target in arr[].

#include <iostream>
#include <climits>

using namespace std;

int countOccurences(int arr[], int size, int target)
{
    int left = 0, right = size - 1;
    while (left <= right)
    {
        int mid = left + (right - left) / 2;
        if (arr[mid] == target)
        {
            int ans = 1;
            // span right
            int r = mid + 1;
            while (r < size && arr[r++] == target)
            {
                ans++;
            }
            // span left
            int l = mid - 1;
            while (l >= 0 && arr[l--] == target)
            {
                ans++;
            }
            return ans;
        }
        if (arr[mid] > target)
        {
            right = mid - 1;
        }
        else
        {
            left = mid + 1;
        }
    }
    return 0;
}

int main()
{
    int arr[] = {8, 9, 10, 12, 12, 12};
    int size = sizeof(arr) / sizeof(arr[0]);
    int target = 12;
    cout << "Number of occurences of " << target << ": " << countOccurences(arr, size, target) << endl;
    return 0;
}