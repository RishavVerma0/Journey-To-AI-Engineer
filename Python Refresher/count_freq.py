def count_characters(text):
    frequency = {}

    for char in text.lower():
        if char.isalpha():
            frequency[char] = frequency.get(char, 0) + 1

    return frequency


text = input("Enter a string: ")

result = count_characters(text)

print("Character frequency:")
for char, count in result.items():
    print(char, ":", count)