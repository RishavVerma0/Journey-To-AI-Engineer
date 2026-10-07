# 301. Remove Invalid Parentheses
# Solved
# Hard
# Topics
# premium lock icon
# Companies
# Hint
# Given a string s that contains parentheses and letters, remove the minimum number of invalid parentheses to make the input string valid.

# Return a list of unique strings that are valid with the minimum number of removals. You may return the answer in any order.

 

# Example 1:

# Input: s = "()())()"
# Output: ["(())()","()()()"]
# Example 2:

# Input: s = "(a)())()"
# Output: ["(a())()","(a)()()"]
# Example 3:

# Input: s = ")("
# Output: [""]



from typing import List


class Solution:
    def removeInvalidParentheses(self, s: str) -> List[str]:
        ans = []
        self.remove(s, ans, 0, 0, ['(', ')'])
        return ans

    def remove(self, s, ans, i, j, p):
        count = 0

        for k in range(i, len(s)):
            if s[k] == p[0]:
                count += 1
            if s[k] == p[1]:
                count -= 1

            if count < 0:
                for x in range(j, k + 1):
                    if s[x] == p[1] and (x == j or s[x - 1] != p[1]):
                        self.remove(s[:x] + s[x + 1:], ans, k, x, p)
                return

        rev = s[::-1]

        if p[0] == '(':
            self.remove(rev, ans, 0, 0, [')', '('])
        else:
            ans.append(rev)