class InsufficientBalanceError(Exception):
    pass


class BankAccount:

    def __init__(self, owner, balance=0):
        self.owner = owner
        self._balance = balance

    @property
    def balance(self):
        return self._balance

    @property
    def account_status(self):
        return "ACTIVE" if self._balance > 0 else "EMPTY"

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit must be positive")

        self._balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal must be positive")

        if amount > self._balance:
            raise InsufficientBalanceError(
                "Insufficient account balance"
            )

        self._balance -= amount

    def __str__(self):
        return (
            f"Owner: {self.owner}\n"
            f"Balance: ₹{self.balance:,.2f}\n"
            f"Status: {self.account_status}"
        )


account = BankAccount("Rishav", 10000)

account.deposit(5000)
account.withdraw(3000)

print(account)

try:
    account.withdraw(20000)
except InsufficientBalanceError as e:
    print("Error:", e)