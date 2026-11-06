class SmartATM:

    def __init__(self, account_holder, balance):
        self.account_holder = account_holder
        self.__balance = balance  # Private attribute

    def check_balance(self):
        print(f"Account Holder: {self.account_holder}")
        print(f"Available Balance: ₹{self.__balance}")

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print(f"₹{amount} deposited successfully.")

    def withdraw(self, amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            print(f"₹{amount} withdrawn successfully.")
        else:
            print("Insufficient balance or invalid amount.")


# Creating objects
user1 = SmartATM("Rishav", 25000)
user2 = SmartATM("Rahul", 15000)

# Performing transactions
user1.check_balance()
user1.deposit(5000)
user1.withdraw(3000)
user1.check_balance()

print("\nSecond Account:")
user2.check_balance()