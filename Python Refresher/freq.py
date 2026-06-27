# I am trying to implement a word frequency counter using dict

def word_frequency(text):
    freq = {}

    for word in text.split():
        word = word.lower()  # Optional: make counting case-insensitive
        freq[word] = freq.get(word, 0) + 1

    return freq

# Example
text = "apple banana apple orange banana apple"
print(word_frequency(text))