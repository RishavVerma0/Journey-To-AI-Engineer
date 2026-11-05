class BankAccount:
    def __init__(self, name, balance):
        self.name = name
        self.__balance = balance

    def check_balance(self):
        print(f"Account Holder: {self.name}")
        print(f"Available Balance: ₹{self.__balance}")

    def deposit(self, amount):
        if amount <= 0:
            print("Invalid deposit amount!")
        else:
            self.__balance += amount
            print(f"₹{amount} deposited successfully.")

    def withdraw(self, amount):
        if amount <= 0:
            print("Invalid withdrawal amount!")
        elif amount > self.__balance:
            print("Insufficient balance!")
        else:
            self.__balance -= amount
            print(f"₹{amount} withdrawn successfully.")

    def transaction_summary(self):
        print("\n--- Transaction Summary ---")
        self.check_balance()


# Creating an account
account = BankAccount("Rishav", 25000)

# Performing transactions
account.check_balance()
account.deposit(5000)
account.withdraw(8000)
account.withdraw(30000)

# Final account summary
account.transaction_summary()