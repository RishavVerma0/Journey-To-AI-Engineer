# emove Duplicates from Sorted Array

# Given a sorted list of integers, remove duplicates in-place so each element appears only once.


def remove_duplicates(nums):
    i = 0

    for j in range(1, len(nums)):
        if nums[j] != nums[i]:
            i += 1
            nums[i] = nums[j]

    return i + 1