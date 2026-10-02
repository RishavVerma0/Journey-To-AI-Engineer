# 22. Generate Parentheses
# Medium
# Topics
# premium lock icon
# Companies
# Given n pairs of parentheses, write a function to generate all combinations of well-formed parentheses.

 

# Example 1:

# Input: n = 3
# Output: ["((()))","(()())","(())()","()(())","()()()"]
# Example 2:

# Input: n = 1
# Output: ["()"]
 

# Constraints:

# 1 <= n <= 8


class Solution:
    def generateParenthesis(self, n: int) -> list[str]:
        if n == 1: return ["()"]

        n -= 1
        res = []

        def dfs(O, C, s):
            if not O and not C:
                res.append(s + ")")
                return

            if O > 0:
                dfs(O - 1, C, s + "(")

            if C >= O:
                dfs(O, C - 1, s + ")")

        dfs(n, n, "(")

        return res