from functools import lru_cache


def max_score(nums):

    @lru_cache(None)
    def dp(left, right):

        if left >= right:
            return 0

        best = 0

        for mid in range(left, right):
            left_sum = sum(nums[left:mid + 1])
            right_sum = sum(nums[mid + 1:right + 1])

            if left_sum < right_sum:
                score = left_sum + dp(left, mid)

            elif right_sum < left_sum:
                score = right_sum + dp(mid + 1, right)

            else:
                score = max(
                    left_sum + dp(left, mid),
                    right_sum + dp(mid + 1, right)
                )

            best = max(best, score)

        return best

    return dp(0, len(nums) - 1)


nums = [6, 2, 3, 4, 5, 5]

print(max_score(nums))