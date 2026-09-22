# 3525. Find X Value of Array II
# Hard
# Topics
# premium lock icon
# Companies
# Hint
# You are given an array of positive integers nums and a positive integer k. You are also given a 2D array queries, where queries[i] = [indexi, valuei, starti, xi].

# You are allowed to perform an operation once on nums, where you can remove any suffix from nums such that nums remains non-empty.

# The x-value of nums for a given x is defined as the number of ways to perform this operation so that the product of the remaining elements leaves a remainder of x modulo k.

# For each query in queries you need to determine the x-value of nums for xi after performing the following actions:

# Update nums[indexi] to valuei. Only this step persists for the rest of the queries.
# Remove the prefix nums[0..(starti - 1)] (where nums[0..(-1)] will be used to represent the empty prefix).
# Return an array result of size queries.length where result[i] is the answer for the ith query.

# A prefix of an array is a subarray that starts from the beginning of the array and extends to any point within it.

# A suffix of an array is a subarray that starts at any point within the array and extends to the end of the array.

# Note that the prefix and suffix to be chosen for the operation can be empty.

# Note that x-value has a different definition in this version.

 

# Example 1:

# Input: nums = [1,2,3,4,5], k = 3, queries = [[2,2,0,2],[3,3,3,0],[0,1,0,1]]

# Output: [2,2,2]

# Explanation:

# For query 0, nums becomes [1, 2, 2, 4, 5], and the empty prefix must be removed. The possible operations are:
# Remove the suffix [2, 4, 5]. nums becomes [1, 2].
# Remove the empty suffix. nums becomes [1, 2, 2, 4, 5] with a product 80, which gives remainder 2 when divided by 3.
# For query 1, nums becomes [1, 2, 2, 3, 5], and the prefix [1, 2, 2] must be removed. The possible operations are:
# Remove the empty suffix. nums becomes [3, 5].
# Remove the suffix [5]. nums becomes [3].
# For query 2, nums becomes [1, 2, 2, 3, 5], and the empty prefix must be removed. The possible operations are:
# Remove the suffix [2, 2, 3, 5]. nums becomes [1].
# Remove the suffix [3, 5]. nums becomes [1, 2, 2].
# Example 2:

# Input: nums = [1,2,4,8,16,32], k = 4, queries = [[0,2,0,2],[0,2,0,1]]

# Output: [1,0]

# Explanation:

# For query 0, nums becomes [2, 2, 4, 8, 16, 32]. The only possible operation is:
# Remove the suffix [2, 4, 8, 16, 32].
# For query 1, nums becomes [2, 2, 4, 8, 16, 32]. There is no possible way to perform the operation.
# Example 3:

# Input: nums = [1,1,2,1,1], k = 2, queries = [[2,1,0,1]]

# Output: [5]

class Solution:
    def resultArray(self, nums, k, queries):
        n = 1

        while n < len(nums):
            n <<= 1

        cnt = [[0] * k for _ in range(2 * n)]
        prod = [1] * (2 * n)

        for i in range(len(nums)):
            r = nums[i] % k
            cnt[n + i][r] = 1
            prod[n + i] = r

        def merge(i):
            l = i * 2
            r = l + 1

            a = cnt[l]
            b = cnt[r]
            c = cnt[i]

            for x in range(k):
                c[x] = a[x]

            for x in range(k):
                if b[x]:
                    y = (prod[l] * x) % k
                    c[y] += b[x]

            prod[i] = (prod[l] * prod[r]) % k

        for i in range(n - 1, 0, -1):
            merge(i)

        def update(idx, val):
            pos = n + idx
            val %= k

            cur = cnt[pos]

            for x in range(k):
                cur[x] = 0

            cur[val] = 1
            prod[pos] = val

            pos //= 2

            while pos:
                merge(pos)
                pos //= 2

        def query(l, r):
            a = [0] * k
            b = [0] * k

            ap = 1
            bp = 1

            l += n
            r += n

            while l < r:
                if l & 1:
                    base = cnt[l]
                    temp = a[:]

                    for x in range(k):
                        if base[x]:
                            y = (ap * x) % k
                            temp[y] += base[x]

                    a = temp
                    ap = (ap * prod[l]) % k
                    l += 1

                if r & 1:
                    r -= 1

                    base = cnt[r]
                    temp = [0] * k

                    for x in range(k):
                        temp[x] = base[x]

                    for x in range(k):
                        if b[x]:
                            y = (prod[r] * x) % k
                            temp[y] += b[x]

                    b = temp
                    bp = (prod[r] * bp) % k

                l //= 2
                r //= 2

            ans = a[:]

            for x in range(k):
                if b[x]:
                    y = (ap * x) % k
                    ans[y] += b[x]

            return ans

        ans = []

        for idx, val, start, x in queries:
            update(idx, val)

            cur = query(start, len(nums))
            ans.append(cur[x])

        return ans