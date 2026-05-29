# 409. Longest Palindrome
# Easy
# Topics
# premium lock icon
# Companies
# Given a string s which consists of lowercase or uppercase letters, return the length of the longest palindrome that can be built with those letters.

# Letters are case sensitive, for example, "Aa" is not considered a palindrome.

 

# Example 1:

# Input: s = "abccccdd"
# Output: 7
# Explanation: One longest palindrome that can be built is "dccaccd", whose length is 7.
# Example 2:

# Input: s = "a"
# Output: 1
# Explanation: The longest palindrome that can be built is "a", whose length is 1.
 

# Constraints:

# 1 <= s.length <= 2000
# s consists of lowercase and/or uppercase English letters only.


class Solution:
    def longestPalindrome(self, s: str) -> int:
        charMap = {}
        for ch in s:
            charMap[ch] = charMap.get(ch,0) + 1
        length = 0
        hasOdd = False
        for count in charMap.values():
            if count & 1 == 0:
                length += count
            else:
                length += count - 1
                hasOdd = True
        if hasOdd:
            length += 1
        return length