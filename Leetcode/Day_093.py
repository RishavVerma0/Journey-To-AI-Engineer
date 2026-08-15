# 3702. Longest Subsequence With Non-Zero Bitwise XOR
# Medium
# Topics
# premium lock icon
# Companies
# Hint
# You are given an integer array nums.

# Return the length of the longest subsequence in nums whose bitwise XOR is non-zero. If no such subsequence exists, return 0.

 

# Example 1:

# Input: nums = [1,2,3]

# Output: 2

# Explanation:

# One longest subsequence is [2, 3]. The bitwise XOR is computed as 2 XOR 3 = 1, which is non-zero.

# Example 2:

# Input: nums = [2,3,4]

# Output: 3

# Explanation:

# The longest subsequence is [2, 3, 4]. The bitwise XOR is computed as 2 XOR 3 XOR 4 = 5, which is non-zero.

 

# Constraints:

# 1 <= nums.length <= 105
# 0 <= nums[i] <= 109


class Solution:
    def longestSubsequence(self, nums):
        total_xor = 0

        for x in nums:
            total_xor ^= x

        # Entire array already has non-zero XOR
        if total_xor != 0:
            return len(nums)

        # XOR is zero, so remove one non-zero element
        for x in nums:
            if x != 0:
                return len(nums) - 1

        # All elements are zero
        return 0