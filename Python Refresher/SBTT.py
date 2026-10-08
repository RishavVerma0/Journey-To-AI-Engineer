class Account:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        self.transactions = []

    def deposit(self, amount):
        self.balance += amount
        self.transactions.append(f"Deposited ₹{amount}")

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            self.transactions.append(f"Withdrawn ₹{amount}")
        else:
            print("Insufficient balance")

    def show_history(self):
        print(f"\nAccount: {self.name}")
        print(f"Balance: ₹{self.balance}")

        for transaction in self.transactions:
            print("-", transaction)


account = Account("Rishav", 10000)

account.deposit(3000)
account.withdraw(1500)
account.withdraw(2000)

account.show_history()