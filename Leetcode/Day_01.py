#Two Sum's most optimal solution is to use a hash map to store the numbers and their indices. 
# This way, we can check if the complement of the current number (target - current number) exists in 
# the hash map in O(1) time. The overall time complexity of this solution is O(n) and the space complexity 
# is also O(n) due to the hash map.

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:

        num_map = {}

        for i, num in enumerate(nums):

            complement = target - num

            if complement in num_map:

                return [num_map[complement], i]

            num_map[num] = i