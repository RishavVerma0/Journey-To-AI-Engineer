def check_even_odd(number):
    if number % 2 == 0:
        return "Even"
    return "Odd"

num = int(input("Enter a number: "))
print(f"{num} is {check_even_odd(num)}")