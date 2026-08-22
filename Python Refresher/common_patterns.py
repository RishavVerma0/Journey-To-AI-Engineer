# Exception handling
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"Error: {e}")
finally:
    print("Done")

# File I/O
with open("example.txt", "w") as f:
    f.write("Hello, file!")

with open("example.txt", "r") as f:
    content = f.read()

# Dict/set comprehensions
squares_dict = {x: x**2 for x in range(5)}

# Unpacking
a, b, *rest = [1, 2, 3, 4, 5]
first, *_, last = [1, 2, 3, 4, 5]

# Enumerate & zip
for i, val in enumerate(["a", "b", "c"]):
    print(i, val)

names = ["Alice", "Bob"]
ages = [30, 25]
for name, age in zip(names, ages):
    print(name, age)

# args & kwargs
def my_func(*args, **kwargs):
    print(args, kwargs)

my_func(1, 2, x=3, y=4)

# Ternary
x = 5
label = "even" if x % 2 == 0 else "odd"