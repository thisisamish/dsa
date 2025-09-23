// Problem Statement: You are given a sorted array containing N integers and a
// number X, you have to find the occurrences of X in the given array.

public class CountOccurencesInSortedArray {
    public static int firstOccurrence(int[] arr, int size, int target) {
        int result = -1;
        int low = 0, high = size - 1;
        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (arr[mid] >= target) {
                if (arr[mid] == target) {
                    result = mid;
                }
                high = mid - 1;
            } else {
                low = mid + 1;
            }
        }
        return result;
    }

    public static int lastOccurrence(int[] arr, int size, int target) {
        int low = 0, high = size - 1;
        int result = -1;
        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (arr[mid] <= target) {
                if (arr[mid] == target) {
                    result = mid;
                }
                low = mid + 1;
            } else {
                high = mid - 1;
            }
        }
        return result;
    }

    public static void main(String[] args) {
        int[] arr = { 1, 2, 4, 5, 5, 5, 6, 6, 7, 8, 9 };
        int size = arr.length;
        int target = 5;
        System.out.println("target: " + target + ", first occurrence: " + firstOccurrence(arr, size, target)
                + ", last occurrence: " + lastOccurrence(arr, size, target));
        target = 3;
        System.out.println("target: " + target + ", first occurrence: " + firstOccurrence(arr, size, target)
                + ", last occurrence: " + lastOccurrence(arr, size, target));
        target = 0;
        System.out.println("target: " + target + ", first occurrence: " + firstOccurrence(arr, size, target)
                + ", last occurrence: " + lastOccurrence(arr, size, target));
        target = 10;
        System.out.println("target: " + target + ", first occurrence: " + firstOccurrence(arr, size, target)
                + ", last occurrence: " + lastOccurrence(arr, size, target));
        target = 8;
        System.out.println("target: " + target + ", first occurrence: " + firstOccurrence(arr, size, target)
                + ", last occurrence: " + lastOccurrence(arr, size, target));
        target = 2;
        System.out.println("target: " + target + ", first occurrence: " + firstOccurrence(arr, size, target)
                + ", last occurrence: " + lastOccurrence(arr, size, target));
        target = 6;
        System.out.println("target: " + target + ", first occurrence: " + firstOccurrence(arr, size, target)
                + ", last occurrence: " + lastOccurrence(arr, size, target));
    }
}
