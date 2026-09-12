# 3414. Maximum Score of Non-overlapping Intervals
# Hard
# Topics
# premium lock icon
# Companies
# Hint
# You are given a 2D integer array intervals, where intervals[i] = [li, ri, weighti]. Interval i starts at position li and ends at ri, and has a weight of weighti. You can choose up to 4 non-overlapping intervals. The score of the chosen intervals is defined as the total sum of their weights.

# Return the lexicographically smallest array of at most 4 indices from intervals with maximum score, representing your choice of non-overlapping intervals.

# Two intervals are said to be non-overlapping if they do not share any points. In particular, intervals sharing a left or right boundary are considered overlapping.

 

# Example 1:

# Input: intervals = [[1,3,2],[4,5,2],[1,5,5],[6,9,3],[6,7,1],[8,9,1]]

# Output: [2,3]

# Explanation:

# You can choose the intervals with indices 2, and 3 with respective weights of 5, and 3.

# Example 2:

# Input: intervals = [[5,8,1],[6,7,7],[4,7,3],[9,10,6],[7,8,2],[11,14,3],[3,5,5]]

# Output: [1,3,5,6]

# Explanation:

# You can choose the intervals with indices 1, 3, 5, and 6 with respective weights of 7, 6, 3, and 5.


from bisect import bisect_left

from git import List


class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        # Store as (end, start, weight, originalIndex) and sort by end boundary
        sortedIntervals = [(r, l, weight, i) for i, (l, r, weight) in enumerate(intervals)]
        sortedIntervals.sort(key=lambda x: x[0])

        # dp[i][j] stores a tuple: (-max_weight, lexicographically_smallest_indices)
        dp = [[(0, []) for _ in range(5)] for _ in range(len(intervals) + 1)]

        for i, (end, start, weight, originalIndex) in enumerate(sortedIntervals):
            # Binary search to find the latest non-overlapping interval
            # bisect_left finds the first interval whose end >= current start
            k = bisect_left(sortedIntervals, (start,), hi=i)
            
            for j in range(1, 5):
                prevWeight, prevIndices = dp[k][j - 1]
                
                skip = dp[i][j]
                
                # min() naturally prioritizes the lowest (most negative) weight sum, 
                # then lexicographically smallest sorted indices
                takeWeight = prevWeight - weight
                takeIndices = sorted(prevIndices + [originalIndex])
                take = (takeWeight, takeIndices)
                
                dp[i + 1][j] = min(skip, take)

        return dp[-1][4][1]