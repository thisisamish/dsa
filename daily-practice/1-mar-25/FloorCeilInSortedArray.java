// Problem Statement:
// You're given an sorted array arr of n integers and an integer x. Find the floor and ceiling of x in arr[0..n-1].
// The floor of x is the largest element in the array which is smaller than or equal to x.
// The ceiling of x is the smallest element in the array greater than or equal to x.

public class FloorCeilInSortedArray {
    public static int floor(int[] arr, int size, int target) {
        int result = -1;
        int low = 0, high = size - 1;
        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (arr[mid] <= target) {
                // search in the right portion since we want the largest element <= target
                result = mid;
                low = mid + 1;
            } else {
                high = mid - 1;
            }
        }
        return result;
    }

    public static int ceil(int[] arr, int size, int target) {
        int result = -1;
        int low = 0, high = size - 1;
        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (arr[mid] >= target) {
                // search in the left portion since we want the smallest element >= target
                result = mid;
                high = mid - 1;
            } else {
                low = mid + 1;
            }
        }
        return result;
    }

    public static void main(String[] args) {
        int[] arr = { 1, 2, 3, 4, 5, 7, 8, 9 };
        int size = arr.length;
        int target = 5;
        System.out.println(
                "target: " + target + ", floor: " + floor(arr, size, target) + ", ceil: " + ceil(arr, size, target));
        target = 6;
        System.out.println(
                "target: " + target + ", floor: " + floor(arr, size, target) + ", ceil: " + ceil(arr, size, target));
        target = 10;
        System.out.println(
                "target: " + target + ", floor: " + floor(arr, size, target) + ", ceil: " + ceil(arr, size, target));
    }
}
