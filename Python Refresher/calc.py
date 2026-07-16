import os

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def calculator():
    while True:
        clear()

        print("=" * 35)
        print("       PYTHON CALCULATOR")
        print("=" * 35)
        print("1. Addition (+)")
        print("2. Subtraction (-)")
        print("3. Multiplication (*)")
        print("4. Division (/)")
        print("5. Modulus (%)")
        print("6. Exponent (^)")
        print("7. Exit")
        print("=" * 35)

        choice = input("Choose an option (1-7): ")

        if choice == "7":
            print("\nThank you for using the calculator!")
            break

        if choice not in ["1", "2", "3", "4", "5", "6"]:
            input("\nInvalid choice! Press Enter to continue...")
            continue

        try:
            num1 = float(input("\nEnter first number: "))
            num2 = float(input("Enter second number: "))

            operator = ""
            result = None

            if choice == "1":
                result = num1 + num2
                operator = "+"

            elif choice == "2":
                result = num1 - num2
                operator = "-"

            elif choice == "3":
                result = num1 * num2
                operator = "*"

            elif choice == "4":
                if num2 == 0:
                    print("\nError: Division by zero!")
                    input("\nPress Enter to continue...")
                    continue
                result = num1 / num2
                operator = "/"

            elif choice == "5":
                result = num1 % num2
                operator = "%"

            elif choice == "6":
                result = num1 ** num2
                operator = "^"

            print("\n" + "-" * 35)
            print(f"Result: {num1} {operator} {num2} = {result}")
            print("-" * 35)

        except ValueError:
            print("\nPlease enter valid numbers!")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    calculator()