def find_largest(numbers):
    largest = numbers[0]

    for num in numbers:
        if num > largest:
            largest = num

    return largest


numbers = list(map(int, input("Enter numbers separated by spaces: ").split()))

print("Largest number:", find_largest(numbers))