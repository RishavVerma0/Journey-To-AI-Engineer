# I am writing a basic python program in which i have to find the maximum element of a list


def find_maxNum(lst):

    if len(lst) == 0:
        return None
    
    maximum = lst[0]

    for i in lst:
        if i > maximum:
            maximum = i

    return maximum

numbers = [1,2,3,4,5]

print(find_maxNum(numbers))