# 877. Stone Game
# Medium
# Topics
# premium lock icon
# Companies
# Alice and Bob play a game with piles of stones. There are an even number of piles arranged in a row, and each pile has a positive integer number of stones piles[i].

# The objective of the game is to end with the most stones. The total number of stones across all the piles is odd, so there are no ties.

# Alice and Bob take turns, with Alice starting first. Each turn, a player takes the entire pile of stones either from the beginning or from the end of the row. This continues until there are no more piles left, at which point the person with the most stones wins.

# Assuming Alice and Bob play optimally, return true if Alice wins the game, or false if Bob wins.

class Solution:
    def stoneGame(self, piles: list[int]) -> bool:
        n = len(piles)

        dp = [[0] * n for _ in range(n)]

        for i in range(n):
            dp[i][i] = piles[i]

        for length in range(2, n + 1):
            for left in range(n - length + 1):
                right = left + length - 1

                take_left = piles[left] - dp[left + 1][right]
                take_right = piles[right] - dp[left][right - 1]

                dp[left][right] = max(take_left, take_right)

        return dp[0][n - 1] > 0