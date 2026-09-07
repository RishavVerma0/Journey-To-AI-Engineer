class ATM:
    bank_name = "Python Bank"
    total_transactions = 0

    def __init__(self, account_holder, balance):
        self.account_holder = account_holder
        self.__balance = balance

    def deposit(self, amount):
        if amount <= 0:
            print("Invalid amount")
            return

        self.__balance += amount
        ATM.total_transactions += 1
        print(f"₹{amount} deposited")

    def withdraw(self, amount):
        if amount <= 0:
            print("Invalid amount")
        elif amount > self.__balance:
            print("Insufficient balance")
        else:
            self.__balance -= amount
            ATM.total_transactions += 1
            print(f"₹{amount} withdrawn")

    def get_balance(self):
        return self.__balance

    @classmethod
    def transaction_count(cls):
        print(f"Total transactions: {cls.total_transactions}")

    @staticmethod
    def is_valid_amount(amount):
        return amount > 0 and amount % 100 == 0


atm1 = ATM("Rishav", 10000)
atm2 = ATM("Aman", 5000)

atm1.deposit(2000)
atm1.withdraw(1000)

atm2.withdraw(1500)

print("Rishav balance:", atm1.get_balance())
print("Aman balance:", atm2.get_balance())

ATM.transaction_count()

print(ATM.is_valid_amount(500))
print(ATM.is_valid_amount(550))