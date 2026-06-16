# 217. Contains Duplicate
# Solved
# Easy
# Topics
# premium lock icon
# Companies
# Given an integer array nums, return true if any value appears at least twice in the array, and return false if every element is distinct.

 

# Example 1:

# Input: nums = [1,2,3,1]

# Output: true

# Explanation:

# The element 1 occurs at the indices 0 and 3.

# Example 2:

# Input: nums = [1,2,3,4]

# Output: false

# Explanation:

# All elements are distinct.

# Example 3:

# Input: nums = [1,1,1,3,3,4,3,2,4,2]

# Output: true

#Solution 1: Step by step
from git import List

class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        seen = set()

        for num in nums:
            if num in seen:
                return True

            seen.add(num)

        return False
    
#Solution 2: One liner answer

class Solution2:
    def containsDuplicate(self, nums: List[int]) -> bool:
        return len(nums) != len(set(nums))