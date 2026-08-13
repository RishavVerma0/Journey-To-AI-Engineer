# 2213. Longest Substring of One Repeating Character
# Hard
# Topics
# premium lock icon
# Companies
# Hint
# You are given a 0-indexed string s. You are also given a 0-indexed string queryCharacters of length k and a 0-indexed array of integer indices queryIndices of length k, both of which are used to describe k queries.

# The ith query updates the character in s at index queryIndices[i] to the character queryCharacters[i].

# Return an array lengths of length k where lengths[i] is the length of the longest substring of s consisting of only one repeating character after the ith query is performed.

 

# Example 1:

# Input: s = "babacc", queryCharacters = "bcb", queryIndices = [1,3,3]
# Output: [3,3,4]
# Explanation: 
# - 1st query updates s = "bbbacc". The longest substring consisting of one repeating character is "bbb" with length 3.
# - 2nd query updates s = "bbbccc". 
#   The longest substring consisting of one repeating character can be "bbb" or "ccc" with length 3.
# - 3rd query updates s = "bbbbcc". The longest substring consisting of one repeating character is "bbbb" with length 4.
# Thus, we return [3,3,4].
# Example 2:

# Input: s = "abyzz", queryCharacters = "aa", queryIndices = [2,1]
# Output: [2,3]
# Explanation:
# - 1st query updates s = "abazz". The longest substring consisting of one repeating character is "zz" with length 2.
# - 2nd query updates s = "aaazz". The longest substring consisting of one repeating character is "aaa" with length 3.
# Thus, we return [2,3].
 

# Constraints:

# 1 <= s.length <= 105
# s consists of lowercase English letters.
# k == queryCharacters.length == queryIndices.length
# 1 <= k <= 105
# queryCharacters consists of lowercase English letters.
# 0 <= queryIndices[i] < s.length


from typing import List

class Solution:
    def longestRepeating(
        self,
        s: str,
        queryCharacters: str,
        queryIndices: List[int]
    ) -> List[int]:

        n = len(s)
        tree = [None] * (4 * n)

        # Node:
        # [left_char, right_char, length,
        #  prefix, suffix, best]

        def merge(left, right):
            if left is None:
                return right

            if right is None:
                return left

            left_char, left_right_char, left_len, left_pre, left_suf, left_best = left
            right_char, right_char_end, right_len, right_pre, right_suf, right_best = right

            length = left_len + right_len

            # Prefix
            prefix = left_pre

            if left_right_char == right_char and left_pre == left_len:
                prefix = left_len + right_pre

            # Suffix
            suffix = right_suf

            if left_right_char == right_char and right_suf == right_len:
                suffix = right_len + left_suf

            # Best answer inside either half
            best = max(left_best, right_best)

            # Possible answer crossing the middle
            if left_right_char == right_char:
                best = max(best, left_suf + right_pre)

            return [
                left_char,
                right_char_end,
                length,
                prefix,
                suffix,
                best
            ]

        def build(node, start, end):
            if start == end:
                tree[node] = [ # type: ignore
                    s[start],   # left char
                    s[start],   # right char
                    1,          # length
                    1,          # prefix
                    1,          # suffix
                    1           # best
                ]
                return

            mid = (start + end) // 2

            build(node * 2, start, mid)
            build(node * 2 + 1, mid + 1, end)

            tree[node] = merge(
                tree[node * 2],
                tree[node * 2 + 1]
            )

        def update(node, start, end, index, char):
            if start == end:
                tree[node] = [ # type: ignore
                    char,
                    char,
                    1,
                    1,
                    1,
                    1
                ]
                return

            mid = (start + end) // 2

            if index <= mid:
                update(node * 2, start, mid, index, char)
            else:
                update(node * 2 + 1, mid + 1, end, index, char)

            tree[node] = merge(
                tree[node * 2],
                tree[node * 2 + 1]
            )

        # Build segment tree
        build(1, 0, n - 1)

        answer = []

        for char, index in zip(queryCharacters, queryIndices):
            update(1, 0, n - 1, index, char)

            # tree[1][5] = longest repeating substring
            answer.append(tree[1][5]) # type: ignore

        return answer