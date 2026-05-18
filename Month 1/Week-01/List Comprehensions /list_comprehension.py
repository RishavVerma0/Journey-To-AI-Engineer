"""
=========================================================
                 PYTHON LIST COMPREHENSION 
=========================================================

This single program demonstrates:

1. Basic list comprehension
2. Conditional list comprehension
3. if-else in list comprehension
4. Nested list comprehension
5. Using functions with list comprehension
6. String processing
7. Flattening nested lists
8. Dictionary comprehension
9. Set comprehension
10. Performance comparison concept

List comprehension provides a short, clean, and efficient
way to create lists in Python.
"""

# ------------------------------------------------------
# 1. BASIC LIST CREATION USING NORMAL LOOP
# ------------------------------------------------------
# Create a list of square numbers using a traditional loop
# ------------------------------------------------------

print("\n1. BASIC FOR LOOP")

squares_loop = []

# Loop through numbers from 1 to 5
for number in range(1, 6):

    # Square the number and store in list
    squares_loop.append(number ** 2)

print("Squares using loop:", squares_loop)


# ------------------------------------------------------
# 2. BASIC LIST COMPREHENSION
# ------------------------------------------------------
# Same operation using list comprehension
# Syntax:
#
# [expression for item in iterable]
# ------------------------------------------------------

print("\n2. BASIC LIST COMPREHENSION")

squares_comprehension = [number ** 2 for number in range(1, 6)]

print("Squares using comprehension:", squares_comprehension)


# ------------------------------------------------------
# Explanation:
# ------------------------------------------------------
# number ** 2     -> expression/output
# for number      -> loop variable
# in range(1, 6)  -> iterable source
# ------------------------------------------------------


# ------------------------------------------------------
# 3. LIST COMPREHENSION WITH CONDITION
# ------------------------------------------------------
# Create a list of even numbers only
# ------------------------------------------------------

print("\n3. CONDITIONAL LIST COMPREHENSION")

even_numbers = [

    number

    # Loop from 1 to 20
    for number in range(1, 21)

    # Include only even numbers
    if number % 2 == 0
]

print("Even numbers:", even_numbers)


# ------------------------------------------------------
# 4. LIST COMPREHENSION WITH IF-ELSE
# ------------------------------------------------------
# Replace even numbers with "EVEN"
# Replace odd numbers with "ODD"
# ------------------------------------------------------

print("\n4. LIST COMPREHENSION WITH IF-ELSE")

number_types = [

    # Expression if condition is TRUE
    "EVEN"

    # Condition check
    if number % 2 == 0

    # Expression if condition is FALSE
    else "ODD"

    # Loop
    for number in range(1, 11)
]

print("Number types:", number_types)


# ------------------------------------------------------
# 5. STRING PROCESSING USING LIST COMPREHENSION
# ------------------------------------------------------
# Convert names to uppercase
# ------------------------------------------------------

print("\n5. STRING PROCESSING")

names = ["john", "alice", "michael", "emma"]

uppercase_names = [

    # Convert each name to uppercase
    name.upper()

    for name in names
]

print("Uppercase names:", uppercase_names)


# ------------------------------------------------------
# 6. FILTER STRINGS BY LENGTH
# ------------------------------------------------------
# Select names longer than 4 characters
# ------------------------------------------------------

print("\n6. FILTERING STRINGS")

long_names = [

    name

    for name in names

    # Keep only names longer than 4 characters
    if len(name) > 4
]

print("Long names:", long_names)


# ------------------------------------------------------
# 7. USING FUNCTIONS INSIDE LIST COMPREHENSION
# ------------------------------------------------------
# Create a reusable function
# ------------------------------------------------------

print("\n7. USING FUNCTIONS")


# Function to calculate cube
def cube(number):

    return number ** 3


# Use function inside list comprehension
cube_values = [

    cube(number)

    for number in range(1, 6)
]

print("Cube values:", cube_values)


# ------------------------------------------------------
# 8. NESTED LIST COMPREHENSION
# ------------------------------------------------------
# Create multiplication table values
# ------------------------------------------------------

print("\n8. NESTED LIST COMPREHENSION")

multiplication_table = [

    # Multiply row and column values
    row * column

    # Outer loop
    for row in range(1, 4)

    # Inner loop
    for column in range(1, 4)
]

print("Multiplication table values:", multiplication_table)


# ------------------------------------------------------
# 9. FLATTENING A NESTED LIST
# ------------------------------------------------------
# Convert 2D list into 1D list
# ------------------------------------------------------

print("\n9. FLATTENING NESTED LIST")

nested_list = [

    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

flattened_list = [

    # Individual item
    item

    # Loop through each sublist
    for sublist in nested_list

    # Loop through items inside sublist
    for item in sublist
]

print("Flattened list:", flattened_list)


# ------------------------------------------------------
# 10. LIST COMPREHENSION WITH MATHEMATICAL OPERATIONS
# ------------------------------------------------------
# Create list of numbers divisible by 3
# ------------------------------------------------------

print("\n10. MATHEMATICAL FILTERING")

divisible_by_three = [

    number

    for number in range(1, 31)

    if number % 3 == 0
]

print("Numbers divisible by 3:", divisible_by_three)


# ------------------------------------------------------
# 11. REMOVE SPACES FROM STRINGS
# ------------------------------------------------------
# Strip whitespace from user data
# ------------------------------------------------------

print("\n11. CLEANING STRING DATA")

raw_data = [

    "  apple ",
    " banana  ",
    "  mango  ",
    "orange "
]

cleaned_data = [

    # Remove extra spaces
    item.strip()

    for item in raw_data
]

print("Cleaned data:", cleaned_data)


# ------------------------------------------------------
# 12. CREATE A MATRIX USING NESTED COMPREHENSION
# ------------------------------------------------------
# Generate 3x3 matrix
# ------------------------------------------------------

print("\n12. MATRIX CREATION")

matrix = [

    # Inner list
    [column for column in range(1, 4)]

    # Outer loop
    for row in range(3)
]

print("Matrix:", matrix)


# ------------------------------------------------------
# 13. DICTIONARY COMPREHENSION
# ------------------------------------------------------
# Create dictionary of squares
# ------------------------------------------------------

print("\n13. DICTIONARY COMPREHENSION")

square_dictionary = {

    # Key : Value
    number: number ** 2

    for number in range(1, 6)
}

print("Square dictionary:", square_dictionary)


# ------------------------------------------------------
# 14. SET COMPREHENSION
# ------------------------------------------------------
# Create unique square values
# ------------------------------------------------------

print("\n14. SET COMPREHENSION")

unique_squares = {

    number ** 2

    for number in [1, 2, 2, 3, 3, 4]
}

print("Unique squares:", unique_squares)


# ------------------------------------------------------
# 15. REAL-WORLD EXAMPLE
# ------------------------------------------------------
# Extract passed students only
# ------------------------------------------------------

print("\n15. REAL-WORLD EXAMPLE")

students = [

    {"name": "John", "marks": 85},
    {"name": "Emma", "marks": 45},
    {"name": "Sophia", "marks": 72},
    {"name": "David", "marks": 30}
]

passed_students = [

    # Store only names
    student["name"]

    for student in students

    # Condition for passing
    if student["marks"] >= 50
]

print("Passed students:", passed_students)


# ------------------------------------------------------
# 16. PERFORMANCE BENEFIT
# ------------------------------------------------------
# List comprehensions are:
#
# - Shorter
# - Cleaner
# - Faster than many traditional loops
#
# They are widely used in:
#
# - Data Science
# - Machine Learning
# - Web Development
# - Automation
# - APIs
# - Data Processing
# ------------------------------------------------------


# ------------------------------------------------------
# 17. IMPORTANT SYNTAX SUMMARY
# ------------------------------------------------------

print("\n17. SYNTAX SUMMARY")

print("""

Basic Syntax:
--------------
[expression for item in iterable]

Conditional Syntax:
-------------------
[expression for item in iterable if condition]

If-Else Syntax:
---------------
[true_value if condition else false_value for item in iterable]

Nested Syntax:
--------------
[expression for item1 in iterable1 for item2 in iterable2]

""")


# ------------------------------------------------------
# 18. FINAL MESSAGE
# ------------------------------------------------------

print("\nProgram completed successfully.")
print("You have learned List Comprehension in Python.")