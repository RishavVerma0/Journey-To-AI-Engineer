from datetime import datetime


class BankAccount:
    bank_name = "Python National Bank"
    total_accounts = 0

    def __init__(self, account_number, holder_name, balance=0):
        self.__account_number = account_number
        self.holder_name = holder_name
        self.__balance = balance
        self.transactions = []

        BankAccount.total_accounts += 1

        self._record_transaction(
            "ACCOUNT_CREATED",
            balance
        )

    # -------------------------
    # PROPERTY: Balance
    # -------------------------

    @property
    def balance(self):
        return self.__balance

    # -------------------------
    # PRIVATE METHOD
    # -------------------------

    def _record_transaction(self, transaction_type, amount):
        self.transactions.append({
            "type": transaction_type,
            "amount": amount,
            "balance_after": self.__balance,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    # -------------------------
    # DEPOSIT
    # -------------------------

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")

        self.__balance += amount

        self._record_transaction(
            "DEPOSIT",
            amount
        )

        print(f"₹{amount} deposited successfully")

    # -------------------------
    # WITHDRAW
    # -------------------------

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")

        if amount > self.__balance:
            raise ValueError("Insufficient balance")

        self.__balance -= amount

        self._record_transaction(
            "WITHDRAW",
            amount
        )

        print(f"₹{amount} withdrawn successfully")

    # -------------------------
    # ACCOUNT DETAILS
    # -------------------------

    def show_details(self):
        print("\n------ ACCOUNT DETAILS ------")
        print(f"Bank      : {self.bank_name}")
        print(f"Account   : {self.__account_number}")
        print(f"Holder    : {self.holder_name}")
        print(f"Balance   : ₹{self.__balance}")
        print("-----------------------------")

    # -------------------------
    # TRANSACTION HISTORY
    # -------------------------

    def show_transactions(self):
        print("\n------ TRANSACTIONS ------")

        for transaction in self.transactions:
            print(
                f"{transaction['time']} | "
                f"{transaction['type']} | "
                f"₹{transaction['amount']} | "
                f"Balance: ₹{transaction['balance_after']}"
            )

    # -------------------------
    # CLASS METHOD
    # -------------------------

    @classmethod
    def get_total_accounts(cls):
        return cls.total_accounts

    # -------------------------
    # STATIC METHOD
    # -------------------------

    @staticmethod
    def is_valid_account_number(account_number):
        return (
            isinstance(account_number, str)
            and account_number.isdigit()
            and len(account_number) == 10
        )


# ============================================================
# SAVINGS ACCOUNT
# ============================================================

class SavingsAccount(BankAccount):

    interest_rate = 0.04

    def __init__(self, account_number, holder_name, balance=0):
        super().__init__(
            account_number,
            holder_name,
            balance
        )

    def calculate_interest(self):
        interest = self.balance * self.interest_rate

        print(
            f"Interest for {self.holder_name}: "
            f"₹{interest:.2f}"
        )

        return interest

    def withdraw(self, amount):
        # Polymorphism:
        # SavingsAccount changes the behaviour
        # of the parent withdraw method.

        minimum_balance = 1000

        if self.balance - amount < minimum_balance:
            raise ValueError(
                f"Minimum balance of ₹{minimum_balance} required"
            )

        super().withdraw(amount)


# ============================================================
# CURRENT ACCOUNT
# ============================================================

class CurrentAccount(BankAccount):

    overdraft_limit = 5000

    def withdraw(self, amount):

        if amount <= self.balance:
            super().withdraw(amount)

        elif amount <= self.balance + self.overdraft_limit:

            overdraft_amount = amount - self.balance

            self._BankAccount__balance = 0

            self._record_transaction(
                "OVERDRAFT",
                overdraft_amount
            )

            print(
                f"₹{amount} withdrawn using overdraft"
            )

        else:
            raise ValueError(
                "Overdraft limit exceeded"
            )


# ============================================================
# CUSTOMER
# ============================================================

class Customer:

    def __init__(self, customer_id, name, email):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.accounts = []

    # Composition:
    # Customer HAS accounts.

    def add_account(self, account):
        self.accounts.append(account)

    def show_accounts(self):

        print(f"\nCustomer: {self.name}")
        print(f"Email   : {self.email}")

        if not self.accounts:
            print("No accounts found")
            return

        for account in self.accounts:

            print(
                f"Account Type: {type(account).__name__}"
            )

            print(
                f"Balance: ₹{account.balance}"
            )


# ============================================================
# BANK
# ============================================================

class Bank:

    def __init__(self, name):
        self.name = name
        self.customers = {}
        self.accounts = {}

    # -------------------------
    # ADD CUSTOMER
    # -------------------------

    def add_customer(self, customer):

        if customer.customer_id in self.customers:
            raise ValueError(
                "Customer already exists"
            )

        self.customers[customer.customer_id] = customer

        print(
            f"Customer {customer.name} added"
        )

    # -------------------------
    # ADD ACCOUNT
    # -------------------------

    def add_account(self, customer_id, account):

        if customer_id not in self.customers:
            raise ValueError(
                "Customer does not exist"
            )

        if account._BankAccount__account_number in self.accounts:
            raise ValueError(
                "Account already exists"
            )

        self.accounts[
            account._BankAccount__account_number
        ] = account

        self.customers[customer_id].add_account(account)

        print(
            f"Account created for "
            f"{self.customers[customer_id].name}"
        )

    # -------------------------
    # FIND ACCOUNT
    # -------------------------

    def find_account(self, account_number):

        account = self.accounts.get(
            account_number
        )

        if account is None:
            raise ValueError(
                "Account not found"
            )

        return account

    # -------------------------
    # TRANSFER MONEY
    # -------------------------

    def transfer(
        self,
        from_account,
        to_account,
        amount
    ):

        sender = self.find_account(
            from_account
        )

        receiver = self.find_account(
            to_account
        )

        if amount <= 0:
            raise ValueError(
                "Transfer amount must be positive"
            )

        sender.withdraw(amount)
        receiver.deposit(amount)

        print(
            f"\n₹{amount} transferred successfully"
        )

    # -------------------------
    # BANK SUMMARY
    # -------------------------

    def show_summary(self):

        print("\n========== BANK SUMMARY ==========")

        print(
            f"Bank      : {self.name}"
        )

        print(
            f"Customers : {len(self.customers)}"
        )

        print(
            f"Accounts  : {len(self.accounts)}"
        )

        total_money = sum(
            account.balance
            for account in self.accounts.values()
        )

        print(
            f"Total Money: ₹{total_money}"
        )

        print("==================================")


# ============================================================
# MAIN PROGRAM
# ============================================================

try:

    # Create bank
    bank = Bank("Python National Bank")

    # Create customers
    customer1 = Customer(
        101,
        "Rishav",
        "rishav@example.com"
    )

    customer2 = Customer(
        102,
        "Aman",
        "aman@example.com"
    )

    # Add customers
    bank.add_customer(customer1)
    bank.add_customer(customer2)

    # Validate account numbers
    account_number_1 = "1234567890"
    account_number_2 = "9876543210"

    if not BankAccount.is_valid_account_number(
        account_number_1
    ):
        raise ValueError(
            "Invalid account number"
        )

    # Create accounts
    savings = SavingsAccount(
        account_number_1,
        "Rishav",
        20000
    )

    current = CurrentAccount(
        account_number_2,
        "Aman",
        10000
    )

    # Add accounts to bank
    bank.add_account(
        101,
        savings
    )

    bank.add_account(
        102,
        current
    )

    # Deposit
    savings.deposit(5000)

    # Withdrawal
    savings.withdraw(3000)

    # Interest
    savings.calculate_interest()

    # Transfer
    bank.transfer(
        account_number_1,
        account_number_2,
        4000
    )

    # Display details
    savings.show_details()
    current.show_details()

    # Transaction history
    savings.show_transactions()
    current.show_transactions()

    # Customer information
    customer1.show_accounts()
    customer2.show_accounts()

    # Bank summary
    bank.show_summary()

    # Class method
    print(
        "\nTotal accounts created:",
        BankAccount.get_total_accounts()
    )

except ValueError as error:

    print(
        f"\nTransaction failed: {error}"
    )

except Exception as error:

    print(
        f"\nUnexpected error: {error}"
    )