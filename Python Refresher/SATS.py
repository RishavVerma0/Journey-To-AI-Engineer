class ATM:
    def __init__(self, pin, balance):
        self.pin = pin
        self.balance = balance
        self.transactions = []

    def verify_pin(self, entered_pin):
        return self.pin == entered_pin

    def deposit(self, amount):
        if amount <= 0:
            print("Invalid deposit amount")
            return

        self.balance += amount
        self.transactions.append(f"Deposited ₹{amount}")
        print("Deposit successful")

    def withdraw(self, amount):
        if amount <= 0:
            print("Invalid withdrawal amount")
        elif amount > self.balance:
            print("Insufficient balance")
        else:
            self.balance -= amount
            self.transactions.append(f"Withdrawn ₹{amount}")
            print("Withdrawal successful")

    def show_balance(self):
        print(f"Available Balance: ₹{self.balance}")

    def show_transactions(self):
        for transaction in self.transactions:
            print(transaction)


atm = ATM(pin=1234, balance=10000)

entered_pin = 1234

if atm.verify_pin(entered_pin):
    atm.deposit(2000)
    atm.withdraw(3500)
    atm.withdraw(20000)

    atm.show_balance()

    print("\nTransaction History:")
    atm.show_transactions()
else:
    print("Incorrect PIN")