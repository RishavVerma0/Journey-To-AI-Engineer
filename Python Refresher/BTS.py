from datetime import datetime


class Transaction:
    def __init__(
        self,
        transaction_type,
        amount,
        balance_after
    ):
        self.transaction_type = transaction_type
        self.amount = amount
        self.balance_after = balance_after

        self.timestamp = (
            datetime.now()
            .strftime("%Y-%m-%d %H:%M:%S")
        )

    def __str__(self):

        return (
            f"{self.timestamp} | "
            f"{self.transaction_type} | "
            f"₹{self.amount:.2f} | "
            f"Balance: ₹{self.balance_after:.2f}"
        )


class BankAccount:

    def __init__(
        self,
        account_number,
        holder_name,
        pin,
        balance=0
    ):
        self.account_number = account_number
        self.holder_name = holder_name

        self.__pin = str(pin)
        self.__balance = balance

        self.transactions = []

    @property
    def balance(self):
        return self.__balance

    def verify_pin(self, pin):

        return self.__pin == str(pin)

    def deposit(self, amount):

        if amount <= 0:
            raise ValueError(
                "Deposit amount must be positive"
            )

        self.__balance += amount

        transaction = Transaction(
            "DEPOSIT",
            amount,
            self.__balance
        )

        self.transactions.append(
            transaction
        )

    def withdraw(self, amount):

        if amount <= 0:
            raise ValueError(
                "Withdrawal amount must be positive"
            )

        if amount > self.__balance:
            raise ValueError(
                "Insufficient balance"
            )

        self.__balance -= amount

        transaction = Transaction(
            "WITHDRAWAL",
            amount,
            self.__balance
        )

        self.transactions.append(
            transaction
        )

    def show_transactions(self):

        print("\n===== TRANSACTIONS =====")

        if not self.transactions:
            print("No transactions")
            return

        for transaction in self.transactions:
            print(transaction)


class SavingsAccount(BankAccount):

    MINIMUM_BALANCE = 1000

    def withdraw(self, amount):

        if self.balance - amount < self.MINIMUM_BALANCE:

            raise ValueError(
                f"Minimum balance of "
                f"₹{self.MINIMUM_BALANCE} required"
            )

        super().withdraw(amount)


class CurrentAccount(BankAccount):

    OVERDRAFT_LIMIT = 5000

    def withdraw(self, amount):

        if amount <= self.balance:

            super().withdraw(amount)
            return

        overdraft_used = (
            amount - self.balance
        )

        if overdraft_used > self.OVERDRAFT_LIMIT:

            raise ValueError(
                "Overdraft limit exceeded"
            )

        # Withdraw existing balance
        existing_balance = self.balance

        if existing_balance > 0:
            super().withdraw(
                existing_balance
            )

        # Record overdraft
        self._BankAccount__balance -= overdraft_used

        transaction = Transaction(
            "OVERDRAFT",
            amount,
            self.balance
        )

        self.transactions.append(
            transaction
        )


class ATM:

    MAX_WITHDRAWAL = 20000
    DAILY_LIMIT = 40000

    def __init__(self, location, cash_available):

        self.location = location
        self.cash_available = cash_available

        self.current_account = None
        self.withdrawn_today = 0

    def insert_card(self, account):

        self.current_account = account

        print(
            f"\nCard inserted for "
            f"{account.holder_name}"
        )

    def authenticate(self, pin):

        if self.current_account is None:
            raise ValueError(
                "Insert card first"
            )

        if not self.current_account.verify_pin(pin):

            raise PermissionError(
                "Incorrect PIN"
            )

        print("Authentication successful")

    def check_balance(self):

        if self.current_account is None:
            raise ValueError(
                "No card inserted"
            )

        print(
            f"Available balance: "
            f"₹{self.current_account.balance:.2f}"
        )

    def withdraw(self, amount):

        if self.current_account is None:
            raise ValueError(
                "Insert card first"
            )

        if amount % 100 != 0:
            raise ValueError(
                "Amount must be a multiple of ₹100"
            )

        if amount > self.MAX_WITHDRAWAL:
            raise ValueError(
                f"Maximum withdrawal is "
                f"₹{self.MAX_WITHDRAWAL}"
            )

        if (
            self.withdrawn_today + amount
            > self.DAILY_LIMIT
        ):
            raise ValueError(
                "Daily withdrawal limit exceeded"
            )

        if amount > self.cash_available:
            raise ValueError(
                "ATM does not have enough cash"
            )

        self.current_account.withdraw(
            amount
        )

        self.cash_available -= amount

        self.withdrawn_today += amount

        print(
            f"\nPlease collect ₹{amount}"
        )

        print(
            f"ATM remaining cash: "
            f"₹{self.cash_available}"
        )

    def deposit(self, amount):

        if self.current_account is None:
            raise ValueError(
                "Insert card first"
            )

        self.current_account.deposit(
            amount
        )

        self.cash_available += amount

        print(
            f"₹{amount} deposited successfully"
        )

    def eject_card(self):

        if self.current_account:

            print(
                f"\nCard ejected for "
                f"{self.current_account.holder_name}"
            )

        self.current_account = None


class Bank:

    def __init__(self, name):

        self.name = name
        self.accounts = {}

    def create_account(
        self,
        account
    ):

        if account.account_number in self.accounts:

            raise ValueError(
                "Account already exists"
            )

        self.accounts[
            account.account_number
        ] = account

        print(
            f"Account created: "
            f"{account.account_number}"
        )

    def find_account(
        self,
        account_number
    ):

        account = self.accounts.get(
            account_number
        )

        if account is None:
            raise ValueError(
                "Account not found"
            )

        return account


# =========================================
# REAL-LIFE USAGE
# =========================================

bank = Bank(
    "Python National Bank"
)


savings = SavingsAccount(
    "1234567890",
    "Rishav",
    1234,
    30000
)


current = CurrentAccount(
    "9876543210",
    "Aman",
    5678,
    10000
)


bank.create_account(
    savings
)

bank.create_account(
    current
)


atm = ATM(
    "Gurugram",
    100000
)


# Insert card

atm.insert_card(
    savings
)


# PIN authentication

atm.authenticate(
    1234
)


# Check balance

atm.check_balance()


# Withdraw

atm.withdraw(
    5000
)


# Deposit

atm.deposit(
    2000
)


# Check balance again

atm.check_balance()


# Transaction history

savings.show_transactions()


# Eject card

atm.eject_card()