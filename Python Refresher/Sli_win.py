def longest_unique_substring(s):
    seen = {}
    left = 0
    max_length = 0
    best_substring = ""

    for right, char in enumerate(s):

        if char in seen and seen[char] >= left:
            left = seen[char] + 1

        seen[char] = right

        current_length = right - left + 1

        if current_length > max_length:
            max_length = current_length
            best_substring = s[left:right + 1]

    return best_substring


s = input("Enter a string: ")

result = longest_unique_substring(s)

print("Longest substring:", result)
print("Length:", len(result))