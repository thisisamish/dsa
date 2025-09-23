// Optimised (hash map) solution
// Time Complexity: O(n)
// Space Complexity: O(n)

package twoSum

func twoSum(nums []int, target int) []int {
	numMap := make(map[int]int) // num : index

	for i, num := range nums {
		complement := target - num

		// Check if complement exists
		if idx, found := numMap[complement]; found {
			return []int{idx, i}
		}

		// Add current number to the map
		numMap[num] = i
	}

	return []int{}
}
