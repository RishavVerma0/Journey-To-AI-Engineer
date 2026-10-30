from collections import Counter

def first_unique_char(text):
    frequency = Counter(text)

    for char in text:
        if frequency[char] == 1:
            return char

    return None

print(first_unique_char("aabbcdeff"))  # c