# 3471. Find the Largest Almost Missing Integer
# Solved
# Easy
# Topics
# premium lock icon
# Companies
# Hint
# You are given an integer array nums and an integer k.

# An integer x is almost missing from nums if x appears in exactly one subarray of size k within nums.

# Return the largest almost missing integer from nums. If no such integer exists, return -1.

# A subarray is a contiguous sequence of elements within an array.
 

# Example 1:

# Input: nums = [3,9,2,1,7], k = 3

# Output: 7

# Explanation:

# 1 appears in 2 subarrays of size 3: [9, 2, 1] and [2, 1, 7].
# 2 appears in 3 subarrays of size 3: [3, 9, 2], [9, 2, 1], [2, 1, 7].
# 3 appears in 1 subarray of size 3: [3, 9, 2].
# 7 appears in 1 subarray of size 3: [2, 1, 7].
# 9 appears in 2 subarrays of size 3: [3, 9, 2], and [9, 2, 1].
# We return 7 since it is the largest integer that appears in exactly one subarray of size k.

# Example 2:

# Input: nums = [3,9,7,2,1,7], k = 4

# Output: 3

# Explanation:

# 1 appears in 2 subarrays of size 4: [9, 7, 2, 1], [7, 2, 1, 7].
# 2 appears in 3 subarrays of size 4: [3, 9, 7, 2], [9, 7, 2, 1], [7, 2, 1, 7].
# 3 appears in 1 subarray of size 4: [3, 9, 7, 2].
# 7 appears in 3 subarrays of size 4: [3, 9, 7, 2], [9, 7, 2, 1], [7, 2, 1, 7].
# 9 appears in 2 subarrays of size 4: [3, 9, 7, 2], [9, 7, 2, 1].
# We return 3 since it is the largest and only integer that appears in exactly one subarray of size k.

# Example 3:

# Input: nums = [0,0], k = 1

# Output: -1

# Explanation:

# There is no integer that appears in only one subarray of size 1.


from typing import List


class Solution:
    def largestInteger(self, A: List[int], k: int) -> int:
        f = [0] * 51
        for x in A:
            f[x] += 1

        res, n = -1, len(A)
        for i, c in enumerate(A):
            if k == n or (f[c]==1 and (k==1 or not i or i+1==n)):
                res = max(res, c)

        return res