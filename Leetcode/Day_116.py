# 3871. Count Commas in Range II
# Solved
# Medium
# Topics
# premium lock icon
# Companies
# Hint
# You are given an integer n.

# Return the total number of commas used when writing all integers from [1, n] (inclusive) in standard number formatting.

# In standard formatting:

# A comma is inserted after every three digits from the right.
# Numbers with fewer than 4 digits contain no commas.
 

# Example 1:

# Input: n = 1002

# Output: 3

# Explanation:

# The numbers "1,000", "1,001", and "1,002" each contain one comma, giving a total of 3.

# Example 2:

# Input: n = 998

# Output: 0

# Explanation:

# ​​​​​​​All numbers from 1 to 998 have fewer than four digits. Therefore, no commas are used.

class Solution:
    def countCommas(self, n: int) -> int:
        k = (len(str(n)) - 1) // 3 # int(log10(n)) // 3 
        return k * (n + 1) - (1000**(k + 1) - 1000) // 999