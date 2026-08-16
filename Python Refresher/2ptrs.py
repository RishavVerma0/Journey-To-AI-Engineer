# Find whether an array contains two numbers whose sum equals target.

def two_sum_sorted(nums, target):
    nums.sort()

    left, right = 0, len(nums) - 1

    while left < right:
        total = nums[left] + nums[right]

        if total == target:
            return True
        elif total < target:
            left += 1
        else:
            right -= 1

    return False


nums = [8, 2, 7, 4, 11]
target = 9

print(two_sum_sorted(nums, target))