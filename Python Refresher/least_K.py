def least_k_frequent(nums, k):
    frequency = {}

    for num in nums:
        frequency[num] = frequency.get(num, 0) + 1

    sorted_nums = sorted(
        frequency,
        key=frequency.get # type: ignore
    ) # type: ignore

    return sorted_nums[:k]


nums = list(map(int, input("Enter numbers: ").split()))
k = int(input("Enter k: "))

print("Least", k, "frequent elements:", least_k_frequent(nums, k))