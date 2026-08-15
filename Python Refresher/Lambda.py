# Sort words primarily by length and then alphabetically when lengths are equal.

def smart_sort(words):
    return sorted(words, key=lambda word: (len(word), word))


words = ["python", "java", "c", "go", "rust", "cpp", "ai"]

result = smart_sort(words)

print(result)