# 5. Longest Palindromic Substring
# Solved
# Medium
# Topics
# premium lock icon
# Companies
# Hint
# Given a string s, return the longest palindromic substring in s.

 

# Example 1:

# Input: s = "babad"
# Output: "bab"
# Explanation: "aba" is also a valid answer.
# Example 2:

# Input: s = "cbbd"
# Output: "bb"
 

# Constraints:

# 1 <= s.length <= 1000
# s consist of only digits and English letters.

class Solution:
    def longestPalindrome(self, s: str) -> str:
        n = len(s)
        res = ""

        for i in range(n):
            # Odd length palindrome
            st = end = i
            while st >= 0 and end < n and s[st] == s[end]:
                st -= 1
                end += 1
            temp = s[st+1:end]
            if len(temp) > len(res):
                res = temp

            # Even length palindrome
            st, end = i, i+1
            while st >= 0 and end < n and s[st] == s[end]:
                st -= 1
                end += 1
            temp = s[st+1:end]
            if len(temp) > len(res):
                res = temp

        return res