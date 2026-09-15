from datetime import datetime


class Restaurant:

    def __init__(self, restaurant_id, name):
        self.restaurant_id = restaurant_id
        self.name = name
        self.menu = {}
        self.is_open = True

    def add_item(self, item_id, name, price):
        self.menu[item_id] = {
            "name": name,
            "price": price
        }

    def remove_item(self, item_id):
        if item_id in self.menu:
            del self.menu[item_id]

    def show_menu(self):
        print(f"\n--- {self.name} MENU ---")

        for item_id, item in self.menu.items():
            print(
                f"{item_id}. {item['name']} - "
                f"₹{item['price']}"
            )

    def get_item(self, item_id):
        if item_id not in self.menu:
            raise ValueError("Item not available")

        return self.menu[item_id]


class Customer:

    def __init__(self, customer_id, name, address):
        self.customer_id = customer_id
        self.name = name
        self.address = address
        self.orders = []

    def add_order(self, order):
        self.orders.append(order)

    def order_history(self):
        print(f"\n--- {self.name}'s Orders ---")

        for order in self.orders:
            print(
                f"Order #{order.order_id} | "
                f"₹{order.total:.2f} | "
                f"{order.status}"
            )


class Order:

    order_count = 1000

    def __init__(self, customer, restaurant):
        Order.order_count += 1

        self.order_id = Order.order_count
        self.customer = customer
        self.restaurant = restaurant
        self.items = []
        self.status = "CREATED"
        self.created_at = datetime.now()

    def add_item(self, item_id, quantity):

        if quantity <= 0:
            raise ValueError(
                "Quantity must be greater than zero"
            )

        item = self.restaurant.get_item(item_id)

        self.items.append({
            "id": item_id,
            "name": item["name"],
            "price": item["price"],
            "quantity": quantity
        })

    @property
    def subtotal(self):

        return sum(
            item["price"] * item["quantity"]
            for item in self.items
        )

    @property
    def delivery_fee(self):

        if self.subtotal >= 500:
            return 0

        return 40

    @property
    def tax(self):

        return self.subtotal * 0.05

    @property
    def total(self):

        return (
            self.subtotal
            + self.delivery_fee
            + self.tax
        )

    def apply_coupon(self, coupon):

        discount = coupon.calculate_discount(
            self.subtotal
        )

        self._discount = discount

        return discount

    def place_order(self):

        if not self.items:
            raise ValueError(
                "Cannot place empty order"
            )

        if not self.restaurant.is_open:
            raise ValueError(
                "Restaurant is closed"
            )

        self.status = "PLACED"

        self.customer.add_order(self)

    def cancel(self):

        if self.status != "PLACED":
            raise ValueError(
                "Only placed orders can be cancelled"
            )

        self.status = "CANCELLED"

    def show_bill(self):

        print("\n========== BILL ==========")

        print(f"Order ID: {self.order_id}")
        print(f"Customer: {self.customer.name}")
        print(f"Restaurant: {self.restaurant.name}")

        print("\nItems:")

        for item in self.items:
            amount = (
                item["price"]
                * item["quantity"]
            )

            print(
                f"{item['name']} x "
                f"{item['quantity']} = ₹{amount}"
            )

        discount = getattr(
            self,
            "_discount",
            0
        )

        print(f"\nSubtotal    : ₹{self.subtotal:.2f}")
        print(f"Delivery    : ₹{self.delivery_fee:.2f}")
        print(f"Tax         : ₹{self.tax:.2f}")
        print(f"Discount    : ₹{discount:.2f}")

        final_amount = (
            self.total - discount
        )

        print(
            f"Final Total : ₹{final_amount:.2f}"
        )

        print(f"Status      : {self.status}")


class Coupon:

    def __init__(self, code, percentage, max_discount):
        self.code = code
        self.percentage = percentage
        self.max_discount = max_discount

    def calculate_discount(self, amount):

        discount = amount * (
            self.percentage / 100
        )

        return min(
            discount,
            self.max_discount
        )


class Payment:

    def __init__(self, order):
        self.order = order
        self.payment_status = "PENDING"

    def pay(self, amount):

        discount = getattr(
            self.order,
            "_discount",
            0
        )

        expected_amount = (
            self.order.total - discount
        )

        if amount != expected_amount:
            raise ValueError(
                f"Expected ₹{expected_amount:.2f}"
            )

        self.payment_status = "SUCCESS"

        print(
            f"\nPayment successful: ₹{amount:.2f}"
        )


# -------------------------------
# REAL-LIFE USAGE
# -------------------------------

restaurant = Restaurant(
    1,
    "Food Corner"
)

restaurant.add_item(
    101,
    "Paneer Roll",
    180
)

restaurant.add_item(
    102,
    "Veg Biryani",
    220
)

restaurant.add_item(
    103,
    "Cold Coffee",
    120
)

restaurant.show_menu()


customer = Customer(
    501,
    "Rishav",
    "Gurugram"
)


order = Order(
    customer,
    restaurant
)

order.add_item(101, 2)
order.add_item(102, 1)
order.add_item(103, 1)


coupon = Coupon(
    "SAVE10",
    10,
    100
)

discount = order.apply_coupon(coupon)

print(
    f"\nCoupon discount: ₹{discount:.2f}"
)


order.place_order()

order.show_bill()


payment = Payment(order)

final_amount = (
    order.total - discount
)

payment.pay(final_amount)

customer.order_history()