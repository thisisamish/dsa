public class RadixSort {
    // TC: O(d(n + k)), SC: O(n), Stable: Yes
    public static void radixSort(int[] arr, int size) {
        // Find the max number of digits in the array
        int maxNum = arr[0];
        for (int num : arr) {
            maxNum = Math.max(maxNum, num);
        }

        // Use counting sort on each digit starting from LSD to MSD
        int exp = 1;
        int[] digits = new int[size];
        int[] sorted = new int[size];
        while (maxNum / exp > 0) {
            int[] count = new int[10];

            // Extract digits and create count array
            for (int i = 0; i < size; i++) {
                digits[i] = (arr[i] / exp) % 10;
                count[digits[i]]++;
            }

            // Create cumulative count array
            for (int i = 1; i < 10; i++) {
                count[i] += count[i - 1];
            }
            // Sort the array based on the digits
            for (int i = size - 1; i >= 0; i--) {
                sorted[--count[digits[i]]] = arr[i];
            }
            // Copy the sorted array back into the original array
            for (int i = 0; i < size; i++) {
                arr[i] = sorted[i];
            }
            System.arraycopy(sorted, 0, arr, 0, size);
            exp *= 10;
        }
    }

    public static void main(String[] args) {
        int[] arr = { 10, 9, 8, 7, 6, 5, 4, 3, 2, 1 };
        int size = arr.length;
        System.err.print("Before sorting: ");
        for (int num : arr) {
            System.out.print(num + " ");
        }
        System.out.println();
        radixSort(arr, size);
        System.err.print("After sorting: ");
        for (int num : arr) {
            System.out.print(num + " ");
        }
        System.out.println();
    }
}
