# 347. Top K Frequent Elements
# Solved
# Medium
# Topics
# premium lock icon
# Companies
# Given an integer array nums and an integer k, return the k most frequent elements. You may return the answer in any order.

 

# Example 1:

# Input: nums = [1,1,1,2,2,3], k = 2

# Output: [1,2]

# Example 2:

# Input: nums = [1], k = 1

# Output: [1]

# Example 3:

# Input: nums = [1,2,1,2,1,2,3,1,3,2], k = 2

# Output: [1,2]

 

# Constraints:

# 1 <= nums.length <= 105
# -104 <= nums[i] <= 104
# k is in the range [1, the number of unique elements in the array].
# It is guaranteed that the answer is unique.


from collections import Counter

class Solution:
    def topKFrequent(self, nums, k):
        freq = Counter(nums)

        bucket = [[] for _ in range(len(nums) + 1)]

        for num, count in freq.items():
            bucket[count].append(num)

        ans = []

        for count in range(len(bucket) - 1, 0, -1):
            for num in bucket[count]:
                ans.append(num)
                if len(ans) == k:
                    return ans