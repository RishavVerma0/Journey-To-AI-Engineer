# 941. Valid Mountain Array
# Solved
# Easy
# Topics
# premium lock icon
# Companies
# Hint
# Given an array of integers arr, return true if and only if it is a valid mountain array.

# Recall that arr is a mountain array if and only if:

# arr.length >= 3
# There exists some i with 0 < i < arr.length - 1 such that:
# arr[0] < arr[1] < ... < arr[i - 1] < arr[i] 
# arr[i] > arr[i + 1] > ... > arr[arr.length - 1]

 

# Example 1:

# Input: arr = [2,1]
# Output: false
# Example 2:

# Input: arr = [3,5,5]
# Output: false
# Example 3:

# Input: arr = [0,3,2,1]
# Output: true


class Solution:
    def validMountainArray(self, arr: List[int]) -> bool:
        n = len(arr)
        i = 0

        # 1. Climb up
        while i+1 < n and arr[i] < arr[i+1]:
            i += 1

        # 2. Peak check: Peak can't be first or last element
        if i == 0 or i == n-1:
            return False

        # 3. Climb down
        while i+1 < n and arr[i] > arr[i+1]:
            i += 1

        # 4. If we reached the end, it's a mountain
        return i == n-1