def find_missing(nums):
    nums.sort()
    missing = []

    for i in range(1, len(nums)):
        start = nums[i - 1] + 1
        end = nums[i]

        for num in range(start, end):
            missing.append(num)

    return missing


nums = list(map(int, input("Enter numbers: ").split()))

print("Missing numbers:", find_missing(nums))