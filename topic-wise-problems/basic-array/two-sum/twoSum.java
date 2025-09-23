// Optimised (hash map) solution
// Time Complexity: O(n)
// Space Complexity: O(n)

import java.util.HashMap;
import java.util.Map;

public class twoSum {
    public int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> numMap = new HashMap<>();

        for (int i = 0; i < nums.length; i++) {
            int complement = target - nums[i];

            // Check if the complement exists
            if (numMap.containsKey(complement)) {
                return new int[] { numMap.get(complement), i };
            }

            // Add current number to the map
            numMap.put(nums[i], i);
        }

        return new int[] {};
    }
}
