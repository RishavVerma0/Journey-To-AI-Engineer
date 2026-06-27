# I am writing a code to find the even numbers from a list

def even_num(nums):
    evens = []

    for num in nums:
        if num % 2 == 0:
            evens.append(num)

    return evens

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(even_num(numbers))