# 3863. Minimum Operations to Sort a String
# Medium
# Topics
# premium lock icon
# Companies
# Hint
# You are given a string s consisting of lowercase English letters.

# In one operation, you can select any substring of s that is not the entire string and sort it in non-descending alphabetical order.

# Return the minimum number of operations required to make s sorted in non-descending order. If it is not possible, return -1.

 

# Example 1:

# Input: s = "dog"

# Output: 1

# Explanation:​​​​​​​

# Sort substring "og" to "go".
# Now, s = "dgo", which is sorted in ascending order. Thus, the answer is 1.
# Example 2:

# Input: s = "card"

# Output: 2

# Explanation:

# Sort substring "car" to "acr", so s = "acrd".
# Sort substring "rd" to "dr", making s = "acdr", which is sorted in ascending order. Thus, the answer is 2.
# Example 3:

# Input: s = "gf"

# Output: -1

# Explanation:

# It is impossible to sort s under the given constraints. Thus, the answer is -1.


from itertools import islice
from operator import le


class Solution:
    def minOperations(self, s: str) -> int:
        if all(map(le, s, s[1:])):  # already sorted
            return 0
        if len(s) == 2:  # only single letters can be sorted, which changes nothing
            return -1

        mid = lambda: islice(s, 1, len(s) - 1)  # the middle, without copying it
        lo, hi = min(mid()), max(mid())
        if s[0] <= min(lo, s[-1]) or max(s[0], hi) <= s[-1]:  # the first letter is the smallest, or the last the largest
            return 1
        return 3 if s[-1] < lo <= hi < s[0] else 2  # the middle sits strictly between the last letter and the first