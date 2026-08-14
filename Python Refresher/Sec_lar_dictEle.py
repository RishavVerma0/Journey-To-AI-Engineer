def second_largest(nums):
    largest = float("-inf")
    second = float("-inf")

    for num in nums:
        if num > largest:
            second = largest
            largest = num
        elif largest > num > second:
            second = num

    return second if second != float("-inf") else None


nums = [12, 5, 8, 12, 20, 7, 20, 15]

print("Second largest:", second_largest(nums))