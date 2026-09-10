class Wallet:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.__balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")

        self.__balance += amount

    def withdraw(self, amount):
        if amount > self.__balance:
            raise ValueError("Insufficient balance")

        self.__balance -= amount

    def get_balance(self):
        return self.__balance

    def __add__(self, other):
        return self.__balance + other.__balance

    def __gt__(self, other):
        return self.__balance > other.__balance

    def __str__(self):
        return f"{self.owner}: ₹{self.__balance}"


wallet1 = Wallet("Rishav", 5000)
wallet2 = Wallet("Aman", 8000)

wallet1.deposit(2000)
wallet2.withdraw(1000)

print(wallet1)
print(wallet2)

print("Combined balance:", wallet1 + wallet2)

if wallet2 > wallet1:
    print("Aman has more money")
else:
    print("Rishav has more money")