def find_gaps(nums):
    nums.sort()
    gaps = []

    for i in range(1, len(nums)):
        difference = nums[i] - nums[i - 1]

        if difference > 1:
            gaps.append((nums[i - 1], nums[i], difference - 1))

    return gaps


nums = list(map(int, input("Enter numbers: ").split()))

for start, end, count in find_gaps(nums):
    print(f"Between {start} and {end}: {count} missing")