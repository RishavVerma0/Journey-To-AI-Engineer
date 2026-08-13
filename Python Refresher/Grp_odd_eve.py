def group_numbers(nums):
    result = {
        "even": [],
        "odd": []
    }

    for num in nums:
        result["even" if num % 2 == 0 else "odd"].append(num)

    return result


nums = list(map(int, input("Enter numbers: ").split()))

groups = group_numbers(nums)

print("Even:", groups["even"])
print("Odd:", groups["odd"])