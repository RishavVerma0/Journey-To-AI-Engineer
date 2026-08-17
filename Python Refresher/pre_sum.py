def build_prefix(nums):
    prefix = [0]

    for num in nums:
        prefix.append(prefix[-1] + num)

    return prefix


def range_sum(prefix, left, right):
    return prefix[right + 1] - prefix[left]


nums = [4, 2, 7, 1, 5]

prefix = build_prefix(nums)

print("Prefix:", prefix)
print("Sum [1, 3]:", range_sum(prefix, 1, 3))
print("Sum [0, 4]:", range_sum(prefix, 0, 4))