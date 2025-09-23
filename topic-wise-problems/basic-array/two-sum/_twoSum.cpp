// Optimised (hash map) solution
// Time Complexity: O(n)
// Space Complexity: O(n)

#include <bits/stdc++.h>

using namespace std;

vector<int> twoSum(vector<int>& nums, int target) {
  unordered_map<int, int> numMap;  // num : index

  for (int i = 0; i < nums.size(); i++) {
    int complement = target - nums[i];

    // Check if complement exists
    if (numMap.find(complement) != numMap.end()) {
      return {numMap[complement], i};
    }

    // Add current number to the map
    numMap[nums[i]] = i;
  }

  return {};
}