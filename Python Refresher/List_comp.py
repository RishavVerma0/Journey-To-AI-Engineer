numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Basic comprehension
squares = [n ** 2 for n in numbers]
print("Squares:", squares)

# With condition (filter)
evens = [n for n in numbers if n % 2 == 0]
print("Evens:", evens)

# With if-else (transform)
labels = ["even" if n % 2 == 0 else "odd" for n in numbers]
print("Labels:", labels)

# Nested comprehension (flatten a matrix)
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened = [num for row in matrix for num in row]
print("Flattened matrix:", flattened)

# Dictionary comprehension
square_map = {n: n ** 2 for n in numbers}
print("Square map:", square_map)

# Set comprehension
unique_remainders = {n % 3 for n in numbers}
print("Unique remainders mod 3:", unique_remainders)

# Comprehension with function call
words = ["hello", "World", "PYTHON", "code"]
capitalized = [w.upper() for w in words]
print("Capitalized:", capitalized)

if __name__ == "__main__":
    print("\nList comprehension refresher complete.")