# 242. Valid Anagram
# Given two strings s and t, return true if t is an anagram of s, and false otherwise.
# An anagram is a word or phrase formed by rearranging the letters of another word or phrase, using all the original letters exactly once.

# Examples:

# * listen → silent
# * evil → vile
# * cinema → iceman
# * dusty → study

# For phrases, spaces and punctuation are usually ignored:

# * “Dormitory” → “Dirty room”
# * “Astronomer” → “Moon starer”
 

# Example 1:

# Input: s = "anagram", t = "nagaram"

# Output: true

# Example 2:

# Input: s = "rat", t = "car"

# Output: false

 

# Constraints:

# 1 <= s.length, t.length <= 5 * 104
# s and t consist of lowercase English letters.

#Solution 
from collections import Counter
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False

        dict_s = Counter(s)
        dict_t = Counter(t)

        return dict_s == dict_t