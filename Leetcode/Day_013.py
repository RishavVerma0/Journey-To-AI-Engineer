# 263. Ugly Number
# Intuition
# An Ugly Number is a positive number whose prime factors only include 2, 3, and 5.

# The idea is simple:

# Keep dividing the number by 2, 3, or 5 whenever possible.
# If after all divisions the number becomes 1, then it is an ugly number.
# If we encounter a factor other than 2, 3, or 5, the number is not ugly.
# Approach
# If n == 0, return False because 0 is not an ugly number.
# Continuously divide n by:

# 2 if divisible by 2
# 3 if divisible by 3
# 5 if divisible by 5
# Stop when:

# n becomes 1 → return True
# n cannot be divided further by 2, 3, or 5 → return False
# Complexity
# Time complexity: O(log n)
# The number keeps reducing by division operations.

# Space complexity: O(1)
# No extra space is used apart from variables.


class Solution:
    def isUgly(self, n: int) -> bool:
        
        if n == 0:
            return False

        while n not in[1,2,3,5]:
            if n%2 == 0:
                n/=2 # type: ignore
            elif n%3 == 0:
                n/=3 # type: ignore
            elif n%5 == 0:
                n/=5 # type: ignore
            else:
                return False
        return True