from abc import ABC, abstractmethod
from datetime import datetime
from uuid import uuid4


# Custom Exceptions
class InsufficientStockError(Exception):
    pass


class PaymentFailedError(Exception):
    pass


# Product Class
class Product:

    def __init__(self, name, price, stock):
        self.product_id = str(uuid4())[:8]
        self.name = name
        self.price = price
        self.__stock = stock

    @property
    def stock(self):
        return self.__stock

    def update_stock(self, quantity):
        if self.__stock + quantity < 0:
            raise InsufficientStockError(
                f"Not enough stock for {self.name}"
            )

        self.__stock += quantity

    def __str__(self):
        return f"{self.name} | ₹{self.price} | Stock: {self.stock}"


# Abstract Payment Class
class Payment(ABC):

    @abstractmethod
    def process_payment(self, amount):
        pass


# Credit Card Payment
class CreditCardPayment(Payment):

    def process_payment(self, amount): # type: ignore
        print(f"Processing credit card payment: ₹{amount}")
        return True


# UPI Payment
class UPIPayment(Payment):

    def process_payment(self, amount): # type: ignore
        print(f"Processing UPI payment: ₹{amount}")
        return True


# Discount Engine
class DiscountEngine:

    @staticmethod
    def calculate_discount(amount, percentage):
        return amount * percentage / 100


# Order Class
class Order:

    def __init__(self, customer_name):
        self.order_id = str(uuid4())[:10]
        self.customer_name = customer_name
        self.items = {}
        self.status = "Pending"
        self.created_at = datetime.now()

    def add_product(self, product, quantity):

        if quantity <= 0:
            raise ValueError("Quantity must be positive.")

        if product.stock < quantity:
            raise InsufficientStockError(
                f"Only {product.stock} units available."
            )

        self.items[product] = (
            self.items.get(product, 0) + quantity
        )

    def calculate_total(self):

        return sum(
            product.price * quantity
            for product, quantity in self.items.items()
        )

    def checkout(self, payment_method, discount=0):

        if not self.items:
            raise ValueError("Cannot checkout an empty order.")

        # Validate stock before payment
        for product, quantity in self.items.items():
            if product.stock < quantity:
                raise InsufficientStockError(
                    f"Insufficient stock for {product.name}"
                )

        total = self.calculate_total()

        discount_amount = DiscountEngine.calculate_discount(
            total, discount
        )

        final_amount = total - discount_amount

        # Process payment
        if payment_method.process_payment(final_amount):

            # Update inventory only after successful payment
            for product, quantity in self.items.items():
                product.update_stock(-quantity)

            self.status = "Completed"

            print("\nOrder Successfully Placed!")
            print(f"Order ID: {self.order_id}")
            print(f"Customer: {self.customer_name}")
            print(f"Original Amount: ₹{total}")
            print(f"Discount: ₹{discount_amount}")
            print(f"Final Amount: ₹{final_amount}")

        else:
            raise PaymentFailedError("Payment unsuccessful!")


# Inventory Management
class InventoryManager:

    def __init__(self):
        self.products = {}

    def add_product(self, product):
        self.products[product.product_id] = product

    def display_inventory(self):

        print("\n--- Available Inventory ---")

        for product in self.products.values():
            print(product)


# Application
inventory = InventoryManager()

laptop = Product("MacBook Air", 85000, 5)
headphones = Product("Wireless Headphones", 3000, 10)

inventory.add_product(laptop)
inventory.add_product(headphones)

# Create customer order
order = Order("Rishav")

order.add_product(laptop, 1)
order.add_product(headphones, 2)

# Checkout
payment = UPIPayment()

try:
    order.checkout(payment, discount=10)

except (InsufficientStockError, PaymentFailedError, ValueError) as error:
    print(f"Order Failed: {error}")

# Updated inventory
inventory.display_inventory()