# I am writing a code to find the even numbers from a list using list comprehension

def even_num(nums):
    return [num for num in nums if num % 2 == 0]

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(even_num(numbers))