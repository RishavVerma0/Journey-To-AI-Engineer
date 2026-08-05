def group_anagrams(words):
    groups = {}

    for word in words:
        key = "".join(sorted(word))

        if key not in groups:
            groups[key] = []

        groups[key].append(word)

    return list(groups.values())


words = input("Enter words: ").split()

result = group_anagrams(words)

print("Grouped anagrams:")
for group in result:
    print(group)