# 3116. Kth Smallest Amount With Single Denomination Combination
# Hard
# Topics
# premium lock icon
# Companies
# Hint
# You are given an integer array coins representing coins of different denominations and an integer k.

# You have an infinite number of coins of each denomination. However, you are not allowed to combine coins of different denominations.

# Return the kth smallest amount that can be made using these coins.

 

# Example 1:

# Input: coins = [3,6,9], k = 3

# Output: 9

# Explanation: The given coins can make the following amounts:
# Coin 3 produces multiples of 3: 3, 6, 9, 12, 15, etc.
# Coin 6 produces multiples of 6: 6, 12, 18, 24, etc.
# Coin 9 produces multiples of 9: 9, 18, 27, 36, etc.
# All of the coins combined produce: 3, 6, 9, 12, 15, etc.

# Example 2:

# Input: coins = [5,2], k = 7

# Output: 12

# Explanation: The given coins can make the following amounts:
# Coin 5 produces multiples of 5: 5, 10, 15, 20, etc.
# Coin 2 produces multiples of 2: 2, 4, 6, 8, 10, 12, etc.
# All of the coins combined produce: 2, 4, 5, 6, 8, 10, 12, 14, 15, etc.


from typing import List
from math import gcd

class Solution:
    def findKthSmallest(self, coins: List[int], k: int) -> int:

        def lcm(a, b):
            return a // gcd(a, b) * b

        # Remove redundant denominations.
        coins = sorted(set(coins))

        # If a coin is a multiple of a smaller coin,
        # it contributes no new amounts.
        useful = []

        for coin in coins:
            if not any(coin % x == 0 for x in useful):
                useful.append(coin)

        coins = useful

        def count(x):
            """Number of valid amounts <= x."""

            n = len(coins)
            total = 0

            # Inclusion-Exclusion over all subsets
            for mask in range(1, 1 << n):
                multiple = 1
                bits = 0
                valid = True

                for i in range(n):
                    if mask & (1 << i):
                        bits += 1
                        multiple = lcm(multiple, coins[i])

                        if multiple > x:
                            valid = False
                            break

                if not valid:
                    continue

                ways = x // multiple

                if bits % 2:
                    total += ways
                else:
                    total -= ways

            return total

        # The answer cannot exceed k * minimum coin.
        left = 1
        right = k * min(coins)

        while left < right:
            mid = (left + right) // 2

            if count(mid) >= k:
                right = mid
            else:
                left = mid + 1

        return left