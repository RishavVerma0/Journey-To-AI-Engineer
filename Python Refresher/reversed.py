### I am writing a code to reverse a list.

def reversed_list(lst):
    reversed_lst = []

    for item in lst:
        reversed_lst = [item] + reversed_lst

    return reversed_lst

numbers = [1,2,3,4,5]

print(reversed_list(numbers))