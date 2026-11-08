from abc import ABC, abstractmethod
from datetime import datetime


# Custom Exception
class FraudDetectedError(Exception):
    pass


# Abstract Transaction Class
class Transaction(ABC):

    def __init__(self, amount, transaction_type):
        self.amount = amount
        self.transaction_type = transaction_type
        self.timestamp = datetime.now()

    @abstractmethod
    def execute(self, account):
        pass


# Deposit Transaction
class Deposit(Transaction):

    def execute(self, account):
        account._update_balance(self.amount)

        account.add_history(
            f"Deposited ₹{self.amount}"
        )

        print("Deposit successful!")


# Withdrawal Transaction
class Withdrawal(Transaction):

    def execute(self, account):
        if self.amount > account.balance:
            raise ValueError("Insufficient balance!")

        account._update_balance(-self.amount)

        account.add_history(
            f"Withdrawn ₹{self.amount}"
        )

        print("Withdrawal successful!")


# Bank Account Class
class BankAccount:

    def __init__(self, account_holder, balance=0):
        self.account_holder = account_holder
        self.__balance = balance
        self.__blocked = False
        self.__transaction_history = []

    @property
    def balance(self):
        return self.__balance

    @property
    def is_blocked(self):
        return self.__blocked

    def _update_balance(self, amount):
        self.__balance += amount

    def add_history(self, transaction):
        self.__transaction_history.append({
            "transaction": transaction,
            "time": datetime.now()
        })

    def get_history(self):
        for item in self.__transaction_history:
            print(item)

    def block_account(self):
        self.__blocked = True
        print("Account temporarily blocked!")


# Fraud Detection System
class FraudDetector:

    def __init__(self, transaction_limit=50000):
        self.transaction_limit = transaction_limit

    @staticmethod
    def is_valid_amount(amount):
        return amount > 0

    def analyze(self, transaction, account):

        if account.is_blocked:
            raise FraudDetectedError("Account is blocked!")

        if not self.is_valid_amount(transaction.amount):
            raise ValueError("Invalid transaction amount!")

        if transaction.amount > self.transaction_limit:
            account.block_account()

            raise FraudDetectedError(
                "Suspicious transaction detected!"
            )

        return True


# Banking System
class BankingSystem:

    def __init__(self):
        self.detector = FraudDetector()
        self.accounts = {}

    def create_account(self, account_number, account):
        self.accounts[account_number] = account

    def process_transaction(self, account_number, transaction):

        account = self.accounts.get(account_number)

        if not account:
            print("Account not found!")
            return

        try:
            self.detector.analyze(transaction, account)
            transaction.execute(account)

            print(f"Current Balance: ₹{account.balance}")

        except (FraudDetectedError, ValueError) as error:
            print(f"Transaction Failed: {error}")


# Application Execution
bank = BankingSystem()

account1 = BankAccount("Rishav", 100000)

bank.create_account("ACC101", account1)

print("----- Normal Transaction -----")

bank.process_transaction(
    "ACC101",
    Deposit(10000, "Deposit")
)

print("\n----- Withdrawal -----")

bank.process_transaction(
    "ACC101",
    Withdrawal(15000, "Withdrawal")
)

print("\n----- Suspicious Transaction -----")

bank.process_transaction(
    "ACC101",
    Withdrawal(75000, "Withdrawal")
)

print("\n----- Transaction History -----")

account1.get_history()