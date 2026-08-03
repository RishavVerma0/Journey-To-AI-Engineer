def longest_subarray(nums, k):
    prefix_sum = 0
    first_seen = {0: -1}
    longest = 0

    for i, num in enumerate(nums):
        prefix_sum += num

        if prefix_sum - k in first_seen:
            length = i - first_seen[prefix_sum - k]
            longest = max(longest, length)

        if prefix_sum not in first_seen:
            first_seen[prefix_sum] = i

    return longest


nums = list(map(int, input("Enter numbers: ").split()))
k = int(input("Enter k: "))

print("Longest subarray length:", longest_subarray(nums, k))