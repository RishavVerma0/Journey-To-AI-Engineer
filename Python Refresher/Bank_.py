class BankAccount:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
        else:
            print("Insufficient balance")

    def show_balance(self):
        print(f"{self.name}: ₹{self.balance}")


account = BankAccount("Rishav", 5000)

account.deposit(2000)
account.withdraw(1500)
account.show_balance()