class BankAccount:

    def __init__(self, account_holder, account_number, balance=0):
        self.account_holder = account_holder
        self.account_number = account_number
        self.balance = balance
        self.transactions = []

    def deposit(self, amount):

        if amount <= 0:
            raise ValueError("Deposit amount must be positive")

        self.balance += amount

        self.transactions.append({
            "type": "deposit",
            "amount": amount,
            "balance_after": self.balance
        })

        print(
            f"₹{amount} deposited successfully."
        )

    def withdraw(self, amount):

        if amount <= 0:
            raise ValueError(
                "Withdrawal amount must be positive"
            )

        if amount > self.balance:
            raise ValueError(
                "Insufficient balance"
            )

        self.balance -= amount

        self.transactions.append({
            "type": "withdraw",
            "amount": amount,
            "balance_after": self.balance
        })

        print(
            f"₹{amount} withdrawn successfully."
        )

    def get_balance(self):
        return self.balance

    def show_transactions(self):

        if not self.transactions:
            print("No transactions found.")
            return

        print("\n========== TRANSACTIONS ==========")

        for transaction in self.transactions:

            print(
                transaction["type"].upper(),
                "| Amount:",
                transaction["amount"],
                "| Balance:",
                transaction["balance_after"]
            )

    def account_summary(self):

        total_deposits = 0
        total_withdrawals = 0

        for transaction in self.transactions:

            if transaction["type"] == "deposit":
                total_deposits += transaction["amount"]

            elif transaction["type"] == "withdraw":
                total_withdrawals += transaction["amount"]

        return {
            "account_holder": self.account_holder,
            "account_number": self.account_number,
            "current_balance": self.balance,
            "total_deposits": total_deposits,
            "total_withdrawals": total_withdrawals,
            "number_of_transactions": len(self.transactions)
        }


def perform_transaction(account, transaction_type, amount):

    try:

        if transaction_type == "deposit":
            account.deposit(amount)

        elif transaction_type == "withdraw":
            account.withdraw(amount)

        else:
            raise ValueError(
                "Invalid transaction type"
            )

    except ValueError as error:

        print(
            "Transaction failed:",
            error
        )


account = BankAccount(
    "Rishav",
    "ACC1001",
    5000
)

print("Initial Balance:")
print(account.get_balance())

perform_transaction(
    account,
    "deposit",
    2000
)

perform_transaction(
    account,
    "withdraw",
    1500
)

perform_transaction(
    account,
    "withdraw",
    10000
)

perform_transaction(
    account,
    "deposit",
    -500
)

perform_transaction(
    account,
    "deposit",
    3000
)

print("\nCurrent Balance:")
print(account.get_balance())

account.show_transactions()

summary = account.account_summary()

print("\n========== ACCOUNT SUMMARY ==========")

for key, value in summary.items():
    print(
        key.replace("_", " ").title(),
        ":",
        value
    )