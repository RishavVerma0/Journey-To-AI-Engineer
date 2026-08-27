# 3720. Lexicographically Smallest Permutation Greater Than Target
# Solved
# Medium
# Topics
# premium lock icon
# Companies
# Hint
# You are given two strings s and target, both having length n, consisting of lowercase English letters.

# Return the lexicographically smallest permutation of s that is strictly greater than target. If no permutation of s is lexicographically strictly greater than target, return an empty string.

# A string a is lexicographically strictly greater than a string b (of the same length) if in the first position where a and b differ, string a has a letter that appears later in the alphabet than the corresponding letter in b.

 

# Example 1:

# Input: s = "abc", target = "bba"

# Output: "bca"

# Explanation:

# The permutations of s (in lexicographical order) are "abc", "acb", "bac", "bca", "cab", and "cba".
# The lexicographically smallest permutation that is strictly greater than target is "bca".
# Example 2:

# Input: s = "leet", target = "code"

# Output: "eelt"

# Explanation:

# The permutations of s (in lexicographical order) are "eelt", "eetl", "elet", "elte", "etel", "etle", "leet", "lete", "ltee", "teel", "tele", and "tlee".
# The lexicographically smallest permutation that is strictly greater than target is "eelt".
# Example 3:

# Input: s = "baba", target = "bbaa"

# Output: ""

# Explanation:

# The permutations of s (in lexicographical order) are "aabb", "abab", "abba", "baab", "baba", and "bbaa".
# None of them is lexicographically strictly greater than target. Therefore, the answer is "".


class Solution:
    def lexGreaterPermutation(self, s: str, target: str) -> str:
        n = len(s)

        # Frequency of characters in s
        cnt = [0] * 26

        for c in s:
            cnt[ord(c) - ord('a')] += 1

        # Try the position where we make the string greater.
        # Rightmost position is preferred.
        for i in range(n - 1, -1, -1):

            # Rebuild the frequency array for this pivot.
            remain = cnt[:]

            # Try to keep target[0 ... i-1] unchanged.
            possible = True

            for j in range(i):
                x = ord(target[j]) - ord('a')

                if remain[x] == 0:
                    possible = False
                    break

                remain[x] -= 1

            if not possible:
                continue

            # At position i, we need the smallest
            # available character strictly greater than target[i].
            target_char = ord(target[i]) - ord('a')

            for c in range(target_char + 1, 26):

                if remain[c] == 0:
                    continue

                ans = target[:i]

                # Make the first difference here.
                ans += chr(ord('a') + c)

                remain[c] -= 1

                # Fill the rest in sorted order.
                for x in range(26):
                    ans += chr(ord('a') + x) * remain[x]

                return ans

        return ""