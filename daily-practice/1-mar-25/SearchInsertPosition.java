public class SearchInsertPosition {
    // Basically, lower bound
    // TC: O(logn)
    // SC: O(1)
    public static int searchInsertPosition(int[] arr, int size, int target) {
        int low = 0, high = size;
        while (low < high) {
            int mid = low + (high - low) / 2;
            if (arr[mid] >= target) {
                high = mid; // since we want the first occurence of arr[i] >= target, we search in left half
            } else {
                low = mid + 1;
            }
        }
        return low; // this could be high too since the loops ends when high == low i.e. low and high converge
    }

    public static void main(String[] args) {
        int[] arr = { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 };
        int size = arr.length;
        int lb = searchInsertPosition(arr, size, 6);
        System.out.println(lb);
        lb = searchInsertPosition(arr, size, 11);
        System.err.println(lb);
    }
}
