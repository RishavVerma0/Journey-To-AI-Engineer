def rotate_list(nums, k):
    if not nums:
        return nums

    k %= len(nums)

    return nums[-k:] + nums[:-k]


nums = list(map(int, input("Enter numbers: ").split()))
k = int(input("Rotate by: "))

print("Rotated:", rotate_list(nums, k))