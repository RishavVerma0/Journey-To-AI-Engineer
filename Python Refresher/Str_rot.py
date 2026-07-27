def are_rotations(s1, s2):
    if len(s1) != len(s2):
        return False

    return s2 in (s1 + s1)


def main():
    first = input("Enter first string: ")
    second = input("Enter second string: ")

    if are_rotations(first, second):
        print("The strings are rotations of each other.")
    else:
        print("The strings are NOT rotations of each other.")


if __name__ == "__main__":
    main()