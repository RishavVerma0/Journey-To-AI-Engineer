# 2267. Check if There Is a Valid Parentheses String Path
# Hard
# Topics
# premium lock icon
# Companies
# Hint
# A parentheses string is a non-empty string consisting only of '(' and ')'. It is valid if any of the following conditions is true:

# It is ().
# It can be written as AB (A concatenated with B), where A and B are valid parentheses strings.
# It can be written as (A), where A is a valid parentheses string.
# You are given an m x n matrix of parentheses grid. A valid parentheses string path in the grid is a path satisfying all of the following conditions:

# The path starts from the upper left cell (0, 0).
# The path ends at the bottom-right cell (m - 1, n - 1).
# The path only ever moves down or right.
# The resulting parentheses string formed by the path is valid.
# Return true if there exists a valid parentheses string path in the grid. Otherwise, return false.

 

# Example 1:


# Input: grid = [["(","(","("],[")","(",")"],["(","(",")"],["(","(",")"]]
# Output: true
# Explanation: The above diagram shows two possible paths that form valid parentheses strings.
# The first path shown results in the valid parentheses string "()(())".
# The second path shown results in the valid parentheses string "((()))".
# Note that there may be other valid parentheses string paths.
# Example 2:


# Input: grid = [[")",")"],["(","("]]
# Output: false
# Explanation: The two possible paths form the parentheses strings "))(" and ")((". Since neither of them are valid parentheses strings, we return false.

class Solution:
    def hasValidPath(self, grid):
        rows = len(grid)
        cols = len(grid[0])

        if grid[0][0] == ')' or grid[rows - 1][cols - 1] == '(':
            return False

        if (rows + cols - 1) % 2 != 0:
            return False

        memo = {}

        def search_path(row, col, balance):
            if grid[row][col] == '(':
                balance += 1
            else:
                balance -= 1

            if balance < 0:
                return False

            if row == rows - 1 and col == cols - 1:
                return balance == 0

            state = (row, col, balance)

            if state in memo:
                return memo[state]

            valid_path = False

            if row + 1 < rows:
                valid_path = search_path(row + 1, col, balance)

            if not valid_path and col + 1 < cols:
                valid_path = search_path(row, col + 1, balance)

            memo[state] = valid_path
            return valid_path

        return search_path(0, 0, 0)