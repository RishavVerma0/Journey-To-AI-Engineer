# Variables & types
name = "Alice"
age = 30
height = 5.6
is_student = False

# f-strings
print(f"{name} is {age} years old")

# Lists, dicts, sets, tuples
fruits = ["apple", "banana", "cherry"]
person = {"name": "Alice", "age": 30}
unique_nums = {1, 2, 3}
coords = (10, 20)

# List comprehension
squares = [x**2 for x in range(10) if x % 2 == 0]

# Loops
for fruit in fruits:
    print(fruit)

for key, value in person.items():
    print(f"{key}: {value}")

i = 0
while i < 5:
    i += 1

# Functions
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print(greet("Bob"))

# Lambda
add = lambda x, y: x + y

# Classes
class Dog:
    def __init__(self, name):
        self.name = name

    def bark(self):
        return f"{self.name} says woof!"

d = Dog("Rex")
print(d.bark())