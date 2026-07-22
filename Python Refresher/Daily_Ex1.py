"""Statement:
    1) list comprehension to square evens 1-10, 
    2) reverse a string without slicing, 
    3) count word frequency in a sentence using a dict."""


def square_evens():
    numbers = [i * i for i in range(1, 11) if i % 2 == 0]
    print("\nSquared even numbers from 1 to 10:")
    print(numbers)


def reverse_string():
    text = input("Enter a string to reverse: ")
    reversed_text = ""

    for char in text:
        reversed_text = char + reversed_text

    print("\nReversed string:")
    print(reversed_text)


def word_frequency():
    sentence = input("Enter a sentence: ")

    frequency = {}

    for word in sentence.lower().split():
        if word in frequency:
            frequency[word] += 1
        else:
            frequency[word] = 1

    print("\nWord Frequency:")
    for word, count in frequency.items():
        print(f"{word}: {count}")


def main():
    while True:
        print("\n===== Python Practice Menu =====")
        print("1. Square Even Numbers (1-10)")
        print("2. Reverse a String")
        print("3. Count Word Frequency")
        print("4. Exit")

        choice = input("\nEnter your choice (1-4): ")

        if choice == "1":
            square_evens()
        elif choice == "2":
            reverse_string()
        elif choice == "3":
            word_frequency()
        elif choice == "4":
            print("\nGoodbye! 👋")
            break
        else:
            print("\nInvalid choice. Please enter a number between 1 and 4.")


if __name__ == "__main__":
    main()