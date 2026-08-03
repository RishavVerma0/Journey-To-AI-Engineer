def merge_intervals(intervals):
    intervals.sort()

    merged = []

    for start, end in intervals:
        if not merged or start > merged[-1][1]:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)

    return merged


n = int(input("Enter number of intervals: "))

intervals = []

for _ in range(n):
    start, end = map(int, input("Enter start and end: ").split())
    intervals.append([start, end])

print("Merged intervals:", merge_intervals(intervals))