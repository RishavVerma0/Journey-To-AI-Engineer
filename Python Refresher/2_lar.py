def second_largest(nums):
    unique_nums = list(set(nums))

    if len(unique_nums) < 2:
        return None

    unique_nums.sort()

    return unique_nums[-2]


nums = list(map(int, input("Enter numbers: ").split()))

result = second_largest(nums)

if result is None:
    print("Second largest number does not exist")
else:
    print("Second largest:", result)