# calculator.py

# This function adds two numbers
def add(a, b):
    return a + b


# This function subtracts two numbers
def subtract(a, b):
    return a - b


# This function multiplies two numbers
def multiply(a, b):
    return a * b


# This block runs only if this file is executed directly
if __name__ == "__main__":
    print("Calculator module is running directly")

    # Testing functions
    print(add(10, 5))
    print(subtract(10, 5))
    print(multiply(10, 5))