def character_frequency(text):
    freq = {}

    for char in text:
        freq[char] = freq.get(char, 0) + 1

    return freq


def main():
    text = input("Enter a string: ")

    frequencies = character_frequency(text)

    print("\nCharacter Frequencies:")
    for char, count in frequencies.items():
        print(f"{char}: {count}")


if __name__ == "__main__":
    main()