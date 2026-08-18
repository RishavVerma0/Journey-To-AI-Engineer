from collections import Counter

nums = [4, 2, 4, 1, 2, 4, 3, 1, 2, 2]

freq = Counter(nums)

# Sort by frequency descending, then number ascending
result = sorted(freq.items(), key=lambda x: (-x[1], x[0]))

print(result)