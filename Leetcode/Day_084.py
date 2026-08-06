# 3345. Smallest Divisible Digit Product I
# Easy
# Topics
# premium lock icon
# Companies
# Hint
# You are given two integers n and t. Return the smallest number greater than or equal to n such that the product of its digits is divisible by t.

 

# Example 1:

# Input: n = 10, t = 2

# Output: 10

# Explanation:

# The digit product of 10 is 0, which is divisible by 2, making it the smallest number greater than or equal to 10 that satisfies the condition.

# Example 2:

# Input: n = 15, t = 3

# Output: 16

# Explanation:

# The digit product of 16 is 6, which is divisible by 3, making it the smallest number greater than or equal to 15 that satisfies the condition.

class Solution:
    def smallestNumber(self, n: int, t: int) -> int:
        while True:
            product = 1
            x = n
            while x:
                product *= x % 10
                x //= 10
            if product % t == 0:
                return n
            n += 1