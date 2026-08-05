def longest_sequence(nums):
    numbers = set(nums)
    longest = 0

    for num in numbers:
        # Start counting only if this is the beginning
        # of a sequence.
        if num - 1 not in numbers:
            current = num
            length = 1

            while current + 1 in numbers:
                current += 1
                length += 1

            longest = max(longest, length)

    return longest


nums = list(map(int, input("Enter numbers: ").split()))

print("Longest consecutive sequence length:",
      longest_sequence(nums))