# Find the longest substring containing at most k distinct characters.

def longest_substring(s, k):
    freq = {}
    left = 0
    best = 0

    for right in range(len(s)):
        freq[s[right]] = freq.get(s[right], 0) + 1

        while len(freq) > k:
            freq[s[left]] -= 1

            if freq[s[left]] == 0:
                del freq[s[left]]

            left += 1

        best = max(best, right - left + 1)

    return best


s = "eceba"
k = 2

print(longest_substring(s, k))