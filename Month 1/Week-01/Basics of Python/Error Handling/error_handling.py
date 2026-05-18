""""
====================================================
             PYTHON ERROR HANDLING 
====================================================

This program demonstrates:

1. try block
2. except block
3. Multiple exception handling
4. else block
5. finally block
6. Custom exceptions
7. Logging errors
8. File handling
9. Input validation
10. Clean program structure

The example simulates a simple bank withdrawal system.
"""

# Import logging module
# Logging is used in real applications instead of print()
import logging


# --------------------------------------------------
# Configure logging system
# --------------------------------------------------
# Errors will be stored in a file named app.log
# This helps developers debug issues later.
# --------------------------------------------------
logging.basicConfig(
    filename="app.log",                # Log file name
    level=logging.ERROR,                # Store ERROR level logs
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# --------------------------------------------------
# Create custom exception
# --------------------------------------------------
# Custom exceptions improve readability and make
# business logic easier to understand.
# --------------------------------------------------
class InsufficientBalanceError(Exception):
    """
    Raised when withdrawal amount exceeds balance.
    """
    pass


# --------------------------------------------------
# BankAccount class
# --------------------------------------------------
class BankAccount:

    # Constructor method
    def __init__(self, owner, balance):

        # Store account owner name
        self.owner = owner

        # Store initial account balance
        self.balance = balance


    # --------------------------------------------------
    # Withdraw money method
    # --------------------------------------------------
    def withdraw(self, amount):

        # Check if amount is negative or zero
        if amount <= 0:

            # Raise built-in ValueError exception
            raise ValueError(
                "Withdrawal amount must be greater than zero."
            )


        # Check if balance is insufficient
        if amount > self.balance:

            # Raise custom exception
            raise InsufficientBalanceError(
                f"Available balance is only {self.balance}"
            )


        # Deduct amount from balance
        self.balance -= amount


        # Return remaining balance
        return self.balance


# --------------------------------------------------
# Main Program
# --------------------------------------------------
try:

    # Create bank account object
    account = BankAccount("John", 5000)


    # Ask user to enter withdrawal amount
    user_input = input("Enter withdrawal amount: ")


    # Convert user input string into integer
    # This can raise ValueError if input is invalid
    amount = int(user_input)


    # Attempt withdrawal
    remaining_balance = account.withdraw(amount)


# --------------------------------------------------
# Handle invalid number input
# --------------------------------------------------
except ValueError as error:

    print("VALUE ERROR:", error)


    # Store error in log file
    logging.error(error)


# --------------------------------------------------
# Handle insufficient balance
# --------------------------------------------------
except InsufficientBalanceError as error:

    print("BALANCE ERROR:", error)


    # Store error in log file
    logging.error(error)


# --------------------------------------------------
# Handle unexpected errors
# --------------------------------------------------
# This catches any unknown exception.
# Usually placed at the end.
# --------------------------------------------------
except Exception as error:

    print("UNEXPECTED ERROR:", error)


    # Store full exception details in log file
    logging.exception("Unexpected system error occurred")


# --------------------------------------------------
# else block
# --------------------------------------------------
# Executes ONLY if no exception occurs.
# --------------------------------------------------
else:

    print("Withdrawal successful.")

    print("Remaining balance:", remaining_balance)


# --------------------------------------------------
# finally block
# --------------------------------------------------
# Always executes whether error occurs or not.
# Typically used for:
# - Closing files
# - Database cleanup
# - Network cleanup
# --------------------------------------------------
finally:

    print("Thank you for using the banking system.")
