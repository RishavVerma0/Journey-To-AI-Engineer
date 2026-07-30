from collections import Counter


def top_k_frequent(nums, k):
    frequency = Counter(nums)

    buckets = [[] for _ in range(len(nums) + 1)]

    for num, count in frequency.items():
        buckets[count].append(num)

    result = []

    for count in range(len(buckets) - 1, 0, -1):
        for num in buckets[count]:
            result.append(num)

            if len(result) == k:
                return result

    return result


nums = list(map(int, input("Enter numbers: ").split()))
k = int(input("Enter k: "))

print("Top k frequent elements:", top_k_frequent(nums, k))