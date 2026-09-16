from datetime import datetime


class Product:

    def __init__(self, product_id, name, price, stock):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock

    def reduce_stock(self, quantity):

        if quantity <= 0:
            raise ValueError("Quantity must be positive")

        if quantity > self.stock:
            raise ValueError(
                f"Only {self.stock} units of {self.name} available"
            )

        self.stock -= quantity

    def increase_stock(self, quantity):

        if quantity <= 0:
            raise ValueError("Quantity must be positive")

        self.stock += quantity

    def __str__(self):
        return (
            f"{self.product_id} | "
            f"{self.name} | "
            f"₹{self.price} | "
            f"Stock: {self.stock}"
        )


class Customer:

    def __init__(self, customer_id, name, email):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.orders = []

    def add_order(self, order):
        self.orders.append(order)

    def show_order_history(self):

        print(f"\n===== {self.name}'s ORDER HISTORY =====")

        if not self.orders:
            print("No orders found")
            return

        for order in self.orders:
            print(
                f"Order #{order.order_id} | "
                f"₹{order.final_amount:.2f} | "
                f"{order.status}"
            )


class CartItem:

    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

    @property
    def total_price(self):
        return self.product.price * self.quantity


class ShoppingCart:

    def __init__(self):
        self.items = {}

    def add_product(self, product, quantity):

        if quantity <= 0:
            raise ValueError(
                "Quantity must be greater than zero"
            )

        current_quantity = self.items.get(
            product.product_id,
            0
        )

        if current_quantity + quantity > product.stock:
            raise ValueError(
                f"Not enough stock for {product.name}"
            )

        self.items[product.product_id] = (
            current_quantity + quantity
        )

        print(
            f"{quantity} x {product.name} "
            f"added to cart"
        )

    def remove_product(self, product_id):

        if product_id not in self.items:
            raise ValueError(
                "Product is not present in cart"
            )

        del self.items[product_id]

    def update_quantity(self, product, quantity):

        if quantity <= 0:
            self.remove_product(product.product_id)
            return

        if quantity > product.stock:
            raise ValueError(
                "Requested quantity exceeds stock"
            )

        self.items[product.product_id] = quantity

    def calculate_total(self, products):

        total = 0

        for product_id, quantity in self.items.items():

            product = products[product_id]

            total += product.price * quantity

        return total

    def show_cart(self, products):

        print("\n========== CART ==========")

        if not self.items:
            print("Cart is empty")
            return

        for product_id, quantity in self.items.items():

            product = products[product_id]

            print(
                f"{product.name} x {quantity} = "
                f"₹{product.price * quantity}"
            )


class Coupon:

    def __init__(
        self,
        code,
        percentage,
        minimum_order,
        maximum_discount
    ):
        self.code = code
        self.percentage = percentage
        self.minimum_order = minimum_order
        self.maximum_discount = maximum_discount

    def calculate_discount(self, amount):

        if amount < self.minimum_order:
            return 0

        discount = amount * self.percentage / 100

        return min(
            discount,
            self.maximum_discount
        )


class Order:

    order_counter = 1000

    def __init__(self, customer, cart, products):

        Order.order_counter += 1

        self.order_id = Order.order_counter
        self.customer = customer
        self.items = {}
        self.status = "CREATED"
        self.created_at = datetime.now()

        for product_id, quantity in cart.items.items():

            product = products[product_id]

            self.items[product] = quantity

        self.subtotal = sum(
            product.price * quantity
            for product, quantity in self.items.items()
        )

        self.discount = 0

        self.delivery_fee = (
            0 if self.subtotal >= 999 else 80
        )

        self.final_amount = (
            self.subtotal
            + self.delivery_fee
        )

    def apply_coupon(self, coupon):

        self.discount = coupon.calculate_discount(
            self.subtotal
        )

        self.final_amount = (
            self.subtotal
            + self.delivery_fee
            - self.discount
        )

    def confirm(self):

        if not self.items:
            raise ValueError(
                "Cannot confirm empty order"
            )

        for product, quantity in self.items.items():
            product.reduce_stock(quantity)

        self.status = "CONFIRMED"

        self.customer.add_order(self)

    def cancel(self):

        if self.status != "CONFIRMED":
            raise ValueError(
                "Only confirmed orders can be cancelled"
            )

        for product, quantity in self.items.items():
            product.increase_stock(quantity)

        self.status = "CANCELLED"

    def show_invoice(self):

        print("\n========== INVOICE ==========")

        print(f"Order ID : {self.order_id}")
        print(f"Customer : {self.customer.name}")
        print(
            f"Date     : "
            f"{self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
        )

        print("\nItems:")

        for product, quantity in self.items.items():

            amount = product.price * quantity

            print(
                f"{product.name} x {quantity} "
                f"= ₹{amount:.2f}"
            )

        print(f"\nSubtotal : ₹{self.subtotal:.2f}")
        print(f"Delivery : ₹{self.delivery_fee:.2f}")
        print(f"Discount : ₹{self.discount:.2f}")
        print(
            f"TOTAL    : ₹{self.final_amount:.2f}"
        )
        print(f"Status   : {self.status}")


class Payment:

    def __init__(self, order):
        self.order = order
        self.status = "PENDING"
        self.transaction_id = None

    def process_payment(self, amount):

        if self.order.status != "CONFIRMED":
            raise ValueError(
                "Order must be confirmed before payment"
            )

        if amount != self.order.final_amount:
            raise ValueError(
                f"Incorrect payment amount. "
                f"Expected ₹{self.order.final_amount:.2f}"
            )

        self.transaction_id = (
            f"TXN{self.order.order_id}"
        )

        self.status = "SUCCESS"

        print(
            f"\nPayment successful"
            f"\nTransaction: {self.transaction_id}"
            f"\nAmount: ₹{amount:.2f}"
        )


# =====================================================
# REAL-LIFE USAGE
# =====================================================

products = {}

products[101] = Product(
    101,
    "Mechanical Keyboard",
    2500,
    10
)

products[102] = Product(
    102,
    "Wireless Mouse",
    1200,
    15
)

products[103] = Product(
    103,
    "USB-C Cable",
    600,
    20
)


customer = Customer(
    501,
    "Rishav",
    "rishav@example.com"
)


cart = ShoppingCart()

cart.add_product(
    products[101],
    1
)

cart.add_product(
    products[102],
    2
)

cart.add_product(
    products[103],
    1
)


cart.show_cart(products)


print(
    "\nCart total:",
    cart.calculate_total(products)
)


coupon = Coupon(
    "SAVE10",
    10,
    2000,
    500
)


order = Order(
    customer,
    cart,
    products
)

order.apply_coupon(coupon)

order.confirm()

order.show_invoice()


payment = Payment(order)

payment.process_payment(
    order.final_amount
)


print("\n===== UPDATED INVENTORY =====")

for product in products.values():
    print(product)


customer.show_order_history()