def move_zeros(nums):
    pos = 0

    for num in nums:
        if num != 0:
            nums[pos] = num
            pos += 1

    while pos < len(nums):
        nums[pos] = 0
        pos += 1

    return nums


nums = [0, 4, 0, 2, 7, 0, 5, 0, 9]

print(move_zeros(nums))