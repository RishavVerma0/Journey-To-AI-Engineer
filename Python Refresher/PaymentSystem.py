class Payment:
    def __init__(self, amount):
        self.__amount = amount

    def get_amount(self):
        return self.__amount

    def process(self):
        raise NotImplementedError


class CreditCardPayment(Payment):
    def process(self):
        fee = self.get_amount() * 0.02
        total = self.get_amount() + fee

        print(f"Credit Card Payment: ₹{total:.2f}")


class UpiPayment(Payment):
    def process(self):
        fee = 0
        total = self.get_amount() + fee

        print(f"UPI Payment: ₹{total:.2f}")


class WalletPayment(Payment):
    def process(self):
        fee = 5
        total = self.get_amount() + fee

        print(f"Wallet Payment: ₹{total:.2f}")


payments = [
    CreditCardPayment(1000),
    UpiPayment(1000),
    WalletPayment(1000)
]

for payment in payments:
    payment.process()