def first_non_repeating(s):
    freq = {}

    for char in s:
        freq[char] = freq.get(char, 0) + 1

    for char in s:
        if freq[char] == 1:
            return char

    return None


def main():
    text = input("Enter a string: ")
    result = first_non_repeating(text)

    if result:
        print("First non-repeating character:", result)
    else:
        print("No unique character found.")


if __name__ == "__main__":
    main()