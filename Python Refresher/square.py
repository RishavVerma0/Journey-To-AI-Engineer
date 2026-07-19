# Function to calculate squares of even numbers

def even_squares(numbers):
    return [num ** 2 for num in numbers if num % 2 == 0]

nums = [1, 2, 3, 4, 5, 6]
result = even_squares(nums)

print("Original:", nums)
print("Even Squares:", result)