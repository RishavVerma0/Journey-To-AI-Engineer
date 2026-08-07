class BankAccount:
    bank_name = "Python Bank"

    def __init__(self, account_no, owner, balance=0):
        self.account_no = account_no
        self.owner = owner
        self.__balance = balance
        self.__transactions = []

    @property
    def balance(self):
        return self.__balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit must be positive")

        self.__balance += amount
        self.__transactions.append(f"Deposited ₹{amount}")

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal must be positive")

        if amount > self.__balance:
            raise ValueError("Insufficient balance")

        self.__balance -= amount
        self.__transactions.append(f"Withdrew ₹{amount}")

    def transfer(self, other, amount):
        self.withdraw(amount)
        other.deposit(amount)

        self.__transactions.append(
            f"Transferred ₹{amount} to {other.owner}"
        )

    def show_transactions(self):
        for transaction in self.__transactions:
            print(transaction)

    def __str__(self):
        return (
            f"Account: {self.account_no}\n"
            f"Owner: {self.owner}\n"
            f"Balance: ₹{self.__balance}"
        )


a1 = BankAccount("A101", "Rishav", 10000)
a2 = BankAccount("A102", "Rahul", 5000)

a1.deposit(2000)
a1.withdraw(1500)
a1.transfer(a2, 3000)

print(a1)
print()

print("Transactions:")
a1.show_transactions()

print("\nRahul's balance:", a2.balance)