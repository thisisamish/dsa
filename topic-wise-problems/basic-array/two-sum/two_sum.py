# Optimised (hash map) solution
# Time Complexity: O(n)
# Space Complexity: O(n)

from typing import List

def twoSum(nums: List[int], target: int) -> List[int]:
    num_map = {}

    for i, num in enumerate(nums):
        complement = target - num

        # Check if complement exists
        if complement in num_map:
            return [num_map[complement], i]
        
        # Add current number to the map
        num_map[num] = i

    return []