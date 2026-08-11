from abc import ABC, abstractmethod


class PaymentMethod(ABC):

    @abstractmethod
    def pay(self, amount):
        pass

    @abstractmethod
    def refund(self, amount):
        pass


class CreditCard(PaymentMethod):

    def pay(self, amount):
        print(f"Paid ₹{amount} using Credit Card")

    def refund(self, amount):
        print(f"Refunded ₹{amount} to Credit Card")


class UPI(PaymentMethod):

    def pay(self, amount):
        print(f"Paid ₹{amount} using UPI")

    def refund(self, amount):
        print(f"Refunded ₹{amount} to UPI")


class Wallet(PaymentMethod):

    def pay(self, amount):
        print(f"Paid ₹{amount} using Wallet")

    def refund(self, amount):
        print(f"Refunded ₹{amount} to Wallet")


class Order:
    def __init__(self, order_id, amount, payment_method):
        self.order_id = order_id
        self.amount = amount
        self.payment_method = payment_method

    def checkout(self):
        print(f"Order #{self.order_id}")
        self.payment_method.pay(self.amount)

    def cancel(self):
        print(f"Canceling order #{self.order_id}")
        self.payment_method.refund(self.amount)


payments = [
    CreditCard(),
    UPI(),
    Wallet()
]

for index, payment in enumerate(payments, start=1):
    order = Order(
        order_id=index,
        amount=1500 * index,
        payment_method=payment
    )

    order.checkout()
    order.cancel()
    print("-" * 30)