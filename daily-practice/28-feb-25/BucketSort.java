import java.util.ArrayList;
import java.util.Collections;

public class BucketSort {
    public static void bucketSort(float[] arr, int n) {
        @SuppressWarnings("unchecked")
        ArrayList<Float>[] bucket = (ArrayList<Float>[]) new ArrayList[n];
        for (int i = 0; i < n; i++) {
            bucket[i] = new ArrayList<>();
        }
        for (int i = 0; i < n; i++) {
            int bucketIndex = (int) arr[i] * n;
            bucket[bucketIndex].add(arr[i]);
        }
        for (int i = 0; i < n; i++) {
            Collections.sort((bucket[i]));
        }
        int index = 0;
        for (int i = 0; i < n; i++) {
            for (int j = 0, size = bucket[i].size(); j < size; j++) {
                arr[index++] = bucket[i].get(j);
            }
        }
    }

    public static void main(String[] args) {
        float[] arr = { (float) 0.42, (float) 0.32, (float) 0.33, (float) 0.52, (float) 0.37, (float) 0.47,
                (float) 0.51 };
        System.out.print("Before sorting: ");
        for (float i : arr) {
            System.out.print(i + " ");
        }
        System.out.println();
        bucketSort(arr, 7);
        System.out.print("After sorting: ");
        for (float i : arr) {
            System.out.print(i + " ");
        }
        System.out.println();
    }
}
