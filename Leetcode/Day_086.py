# 3302. Find the Lexicographically Smallest Valid Sequence
# Medium
# Topics
# premium lock icon
# Companies
# Hint
# You are given two strings word1 and word2.

# A string x is called almost equal to y if you can change at most one character in x to make it identical to y.

# A sequence of indices seq is called valid if:

# The indices are sorted in ascending order.
# Concatenating the characters at these indices in word1 in the same order results in a string that is almost equal to word2.
# Return an array of size word2.length representing the lexicographically smallest valid sequence of indices. If no such sequence of indices exists, return an empty array.

# Note that the answer must represent the lexicographically smallest array, not the corresponding string formed by those indices.

 

# Example 1:

# Input: word1 = "vbcca", word2 = "abc"

# Output: [0,1,2]

# Explanation:

# The lexicographically smallest valid sequence of indices is [0, 1, 2]:

# Change word1[0] to 'a'.
# word1[1] is already 'b'.
# word1[2] is already 'c'.
# Example 2:

# Input: word1 = "bacdc", word2 = "abc"

# Output: [1,2,4]

# Explanation:

# The lexicographically smallest valid sequence of indices is [1, 2, 4]:

# word1[1] is already 'a'.
# Change word1[2] to 'b'.
# word1[4] is already 'c'.
# Example 3:

# Input: word1 = "aaaaaa", word2 = "aaabc"

# Output: []

# Explanation:

# There is no valid sequence of indices.

# Example 4:

# Input: word1 = "abc", word2 = "ab"

# Output: [0,1]

 

# Constraints:

# 1 <= word2.length < word1.length <= 3 * 105
# word1 and word2 consist only of lowercase English letters.


class Solution:
    def validSequence(self, word1: str, word2: str) -> list[int]:
        n = len(word1)
        m = len(word2)

        # suffix[i] = how many characters of word2 can be
        # matched starting from word1[i] using exact matches.
        suffix = [0] * (n + 1)

        j = m - 1

        for i in range(n - 1, -1, -1):
            if j >= 0 and word1[i] == word2[j]:
                suffix[i] = suffix[i + 1] + 1
                j -= 1
            else:
                suffix[i] = suffix[i + 1]

        ans = []
        start = 0
        used_mismatch = False

        for j in range(m):
            for i in range(start, n):
                # Exact match
                if word1[i] == word2[j]:
                    if suffix[i + 1] >= m - j - 1:
                        ans.append(i)
                        start = i + 1
                        break

                # Use our one allowed mismatch
                elif not used_mismatch:
                    if suffix[i + 1] >= m - j - 1:
                        ans.append(i)
                        start = i + 1
                        used_mismatch = True
                        break
            else:
                return []

        return ans