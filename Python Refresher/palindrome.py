

def pal(str):

    n = len(str)

    for i in range(n // 2):
        if str[i] != str[n - 1 - i]:
            return False
        
    return True


word = input("Enter a string: ")

if pal(word):
    print("Palindrome")

else:
    print("Not a palindrome")



