public class HeapSort {
    interface Heap {
        void insert(int value);

        int pop();

        int peek();

        int size();
    }

    public static class MinHeap implements Heap {
        private int[] heap;
        private int size;
        private int capacity;

        public MinHeap(int capacity) {
            this.capacity = capacity;
            this.heap = new int[capacity];
            this.size = 0;
        }

        private int parent(int i) {
            return (i - 1) / 2;
        }

        private int left(int i) {
            return 2 * i + 1;
        }

        private int right(int i) {
            return 2 * i + 2;
        }

        @Override
        public void insert(int value) {
            if (size == capacity) {
                throw new IllegalStateException("Heap is full!");
            }

            heap[size] = value;
            int current = size;
            size++;

            while (current > 0 && heap[current] < heap[parent(current)]) {
                swap(current, parent(current));
                current = parent(current);
            }
        }

        @Override
        public int pop() {
            if (size == 0) {
                throw new IllegalStateException("Heap is empty!");
            }
            int min = heap[0];
            heap[0] = heap[size - 1];
            size--;
            heapify(0);
            return min;
        }

        @Override
        public int peek() {
            if (size == 0) {
                throw new IllegalStateException("Heap is empty!");
            }
            return heap[0];
        }

        @Override
        public int size() {
            return size;
        }

        private void heapify(int i) {
            int smallest = i;
            int left = left(i);
            int right = right(i);

            if (left < size && heap[left] < heap[smallest]) {
                smallest = left;
            }
            if (right < size && heap[right] < heap[smallest]) {
                smallest = right;
            }
            if (smallest != i) {
                swap(i, smallest);
                heapify(smallest);
            }
        }

        private void swap(int i, int j) {
            int temp = heap[i];
            heap[i] = heap[j];
            heap[j] = temp;
        }

        public void buildHeap(int[] array) {
            if (array.length > capacity) {
                throw new IllegalArgumentException("Array size exceeds heap capacity!");
            }
            System.arraycopy(array, 0, heap, 0, array.length);
            size = array.length;
            for (int i = parent(size - 1); i >= 0; i--) {
                heapify(i);
            }
        }

        public int[] heapSort() {
            int originalSize = size;
            int[] sorted = new int[size];
            for (int i = 0; i < sorted.length; i++) {
                sorted[i] = pop();
            }
            size = originalSize;
            return sorted;
        }
    }

    public static void main(String[] args) {
        int[] array = { 10, 3, 76, 34, 23, 32 };
        System.out.print("Before sorting:");
        for (int value : array) {
            System.out.print(value + " ");
        }
        System.out.println();
        MinHeap minHeap = new MinHeap(array.length);
        minHeap.buildHeap(array);
        int[] sortedArray = minHeap.heapSort();
        System.out.print("After sorting:");
        for (int value : sortedArray) {
            System.out.print(value + " ");
        }
        System.out.println();
    }
}
