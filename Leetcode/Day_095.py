# 1563. Stone Game V
# Hard
# Topics
# premium lock icon
# Companies
# Hint
# There are several stones arranged in a row, and each stone has an associated value which is an integer given in the array stoneValue.

# In each round of the game, Alice divides the row into two non-empty rows (i.e. left row and right row), then Bob calculates the value of each row which is the sum of the values of all the stones in this row. Bob throws away the row which has the maximum value, and Alice's score increases by the value of the remaining row. If the value of the two rows are equal, Bob lets Alice decide which row will be thrown away. The next round starts with the remaining row.

# The game ends when there is only one stone remaining. Alice's score is initially zero.

# Return the maximum score that Alice can obtain.

 

# Example 1:

# Input: stoneValue = [6,2,3,4,5,5]
# Output: 18
# Explanation: In the first round, Alice divides the row to [6,2,3], [4,5,5]. The left row has the value 11 and the right row has value 14. Bob throws away the right row and Alice's score is now 11.
# In the second round Alice divides the row to [6], [2,3]. This time Bob throws away the left row and Alice's score becomes 16 (11 + 5).
# The last round Alice has only one choice to divide the row which is [2], [3]. Bob throws away the right row and Alice's score is now 18 (16 + 2). The game ends because only one stone is remaining in the row.
# Example 2:

# Input: stoneValue = [7,7,7,7,7,7,7]
# Output: 28
# Example 3:

# Input: stoneValue = [4]
# Output: 0
 

# Constraints:

# 1 <= stoneValue.length <= 500
# 1 <= stoneValue[i] <= 106


from typing import List


class Solution:
    def stoneGameV(self, stoneValue: List[int]) -> int:
        n = len(stoneValue)

        # Prefix sum
        prefix = [0] * (n + 1)
        for i in range(n):
            prefix[i + 1] = prefix[i] + stoneValue[i]

        def range_sum(l, r):
            return prefix[r + 1] - prefix[l]

        # dp[l][r] = maximum score for stones l...r
        dp = [[0] * n for _ in range(n)]

        # Length of interval
        for length in range(2, n + 1):
            for l in range(n - length + 1):
                r = l + length - 1

                for k in range(l, r):
                    left = range_sum(l, k)
                    right = range_sum(k + 1, r)

                    if left < right:
                        dp[l][r] = max(
                            dp[l][r],
                            left + dp[l][k]
                        )

                    elif left > right:
                        dp[l][r] = max(
                            dp[l][r],
                            right + dp[k + 1][r]
                        )

                    else:
                        dp[l][r] = max(
                            dp[l][r],
                            left + dp[l][k],
                            right + dp[k + 1][r]
                        )

        return dp[0][n - 1]