def count_letters(text):
    vowels = "aeiou"
    vowel_count = 0
    consonant_count = 0

    for char in text.lower():
        if char.isalpha():
            if char in vowels:
                vowel_count += 1
            else:
                consonant_count += 1

    return vowel_count, consonant_count


text = input("Enter a string: ")

vowels, consonants = count_letters(text)

print("Vowels:", vowels)
print("Consonants:", consonants)