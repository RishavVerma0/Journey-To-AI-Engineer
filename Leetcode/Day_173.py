# 3505. Minimum Operations to Make Elements Within K Subarrays Equal
# Hard
# Topics
# premium lock icon
# Companies
# Hint
# You are given an integer array nums and two integers, x and k. You can perform the following operation any number of times (including zero):

# Increase or decrease any element of nums by 1.
# Return the minimum number of operations needed to have at least k non-overlapping subarrays of size exactly x in nums, where all elements within each subarray are equal.

 

# Example 1:

# Input: nums = [5,-2,1,3,7,3,6,4,-1], x = 3, k = 2

# Output: 8

# Explanation:

# Use 3 operations to add 3 to nums[1] and use 2 operations to subtract 2 from nums[3]. The resulting array is [5, 1, 1, 1, 7, 3, 6, 4, -1].
# Use 1 operation to add 1 to nums[5] and use 2 operations to subtract 2 from nums[6]. The resulting array is [5, 1, 1, 1, 7, 4, 4, 4, -1].
# Now, all elements within each subarray [1, 1, 1] (from indices 1 to 3) and [4, 4, 4] (from indices 5 to 7) are equal. Since 8 total operations were used, 8 is the output.
# Example 2:

# Input: nums = [9,-2,-2,-2,1,5], x = 2, k = 2

# Output: 3

# Explanation:

# Use 3 operations to subtract 3 from nums[4]. The resulting array is [9, -2, -2, -2, -2, 5].
# Now, all elements within each subarray [-2, -2] (from indices 1 to 2) and [-2, -2] (from indices 3 to 4) are equal. Since 3 operations were used, 3 is the output.
 

# Constraints:

# 2 <= nums.length <= 105
# -106 <= nums[i] <= 106
# 2 <= x <= nums.length
# 1 <= k <= 15
# 2 <= k * x <= nums.length


from git import List


class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)
        vals = sorted(set(nums))
        m = len(vals)
        idx = {v: i + 1 for i, v in enumerate(vals)}
        rk = [idx[v] for v in nums]

        bc = [0] * (m + 1)
        bs = [0] * (m + 1)
        cnt_at = [0] * (m + 1)
        LOG = m.bit_length()
        need = (x + 1) // 2

        def upd(i, c, v):
            while i <= m:
                bc[i] += c
                bs[i] += v
                i += i & -i

        tot = 0
        for i in range(x):
            upd(rk[i], 1, nums[i])
            cnt_at[rk[i]] += 1
            tot += nums[i]

        cost = [0] * (n - x + 1)
        for s in range(n - x + 1):
            pos, kk, acc_c, acc_s = 0, need, 0, 0
            for b in range(LOG, -1, -1):
                np_ = pos + (1 << b)
                if np_ <= m and bc[np_] < kk:
                    pos = np_
                    kk -= bc[np_]
                    acc_c += bc[np_]
                    acc_s += bs[np_]
            p = pos + 1
            med = vals[p - 1]
            cnt_le = acc_c + cnt_at[p]
            sum_le = acc_s + cnt_at[p] * med
            cost[s] = med * cnt_le - sum_le + (tot - sum_le) - med * (x - cnt_le)

            upd(rk[s], -1, -nums[s])
            cnt_at[rk[s]] -= 1
            tot -= nums[s]
            if s + x < n:
                upd(rk[s + x], 1, nums[s + x])
                cnt_at[rk[s + x]] += 1
                tot += nums[s + x]

        INF = float('inf')
        prev = [0] * (n + 1)
        for _ in range(k):
            cur = [INF] * (n + 1)
            for i in range(x, n + 1):
                cur[i] = min(cur[i - 1], prev[i - x] + cost[i - x])
            prev = cur
        return prev[n] # type: ignore