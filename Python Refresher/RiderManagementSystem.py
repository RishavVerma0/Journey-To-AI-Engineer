from datetime import datetime


class Location:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def distance_to(self, other):

        lat_difference = (
            self.latitude - other.latitude
        )

        lon_difference = (
            self.longitude - other.longitude
        )

        return (
            lat_difference ** 2
            + lon_difference ** 2
        ) ** 0.5


class Restaurant:
    def __init__(
        self,
        restaurant_id,
        name,
        location
    ):
        self.restaurant_id = restaurant_id
        self.name = name
        self.location = location

        self.menu = {}
        self.orders = []

    def add_food(
        self,
        food_id,
        name,
        price
    ):

        self.menu[food_id] = {
            "name": name,
            "price": price
        }

    def get_food(self, food_id):

        if food_id not in self.menu:
            raise ValueError(
                "Food item not found"
            )

        return self.menu[food_id]

    def receive_order(self, order):

        self.orders.append(order)


class Customer:
    def __init__(
        self,
        customer_id,
        name,
        location
    ):
        self.customer_id = customer_id
        self.name = name
        self.location = location

        self.orders = []

    def add_order(self, order):
        self.orders.append(order)


class Rider:
    def __init__(
        self,
        rider_id,
        name,
        location
    ):
        self.rider_id = rider_id
        self.name = name
        self.location = location

        self.available = True
        self.total_deliveries = 0
        self.total_earnings = 0

    def distance_from(self, location):
        return self.location.distance_to(
            location
        )

    def assign_order(self):

        if not self.available:
            raise ValueError(
                "Rider is already busy"
            )

        self.available = False

    def complete_delivery(
        self,
        earnings,
        destination
    ):

        self.location = destination

        self.available = True

        self.total_deliveries += 1

        self.total_earnings += earnings


class OrderItem:
    def __init__(
        self,
        food,
        quantity
    ):
        self.name = food["name"]
        self.price = food["price"]
        self.quantity = quantity

    @property
    def total(self):
        return self.price * self.quantity


class Order:

    counter = 1000

    def __init__(
        self,
        customer,
        restaurant
    ):

        Order.counter += 1

        self.order_id = Order.counter

        self.customer = customer
        self.restaurant = restaurant

        self.items = []

        self.rider = None

        self.status = "CREATED"

        self.created_at = datetime.now()

    def add_item(
        self,
        food,
        quantity
    ):

        if quantity <= 0:
            raise ValueError(
                "Quantity must be positive"
            )

        item = OrderItem(
            food,
            quantity
        )

        self.items.append(item)

    @property
    def subtotal(self):

        return sum(
            item.total
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

    def confirm(self):

        if not self.items:
            raise ValueError(
                "Cannot confirm empty order"
            )

        self.status = "CONFIRMED"

        self.restaurant.receive_order(
            self
        )

        self.customer.add_order(
            self
        )

    def assign_rider(self, rider):

        if self.status != "CONFIRMED":
            raise ValueError(
                "Order must be confirmed first"
            )

        rider.assign_order()

        self.rider = rider

        self.status = "OUT_FOR_DELIVERY"

    def deliver(self):

        if self.rider is None:
            raise ValueError(
                "No rider assigned"
            )

        if self.status != "OUT_FOR_DELIVERY":
            raise ValueError(
                "Order is not out for delivery"
            )

        self.rider.complete_delivery(
            earnings=50,
            destination=self.customer.location
        )

        self.status = "DELIVERED"

    def cancel(self):

        if self.status == "DELIVERED":
            raise ValueError(
                "Delivered order cannot be cancelled"
            )

        if self.rider:
            self.rider.available = True

        self.status = "CANCELLED"

    def print_invoice(self):

        print(
            "\n========== ORDER =========="
        )

        print(
            f"Order ID    : {self.order_id}"
        )

        print(
            f"Customer    : {self.customer.name}"
        )

        print(
            f"Restaurant  : {self.restaurant.name}"
        )

        print("\nItems:")

        for item in self.items:

            print(
                f"{item.name} x "
                f"{item.quantity} = "
                f"₹{item.total}"
            )

        print(
            f"\nSubtotal    : ₹{self.subtotal:.2f}"
        )

        print(
            f"Delivery    : ₹{self.delivery_fee:.2f}"
        )

        print(
            f"Tax         : ₹{self.tax:.2f}"
        )

        print(
            f"Total       : ₹{self.total:.2f}"
        )

        print(
            f"Status      : {self.status}"
        )


class DeliverySystem:

    def __init__(self):

        self.restaurants = {}
        self.customers = {}
        self.riders = {}
        self.orders = {}

    def add_restaurant(
        self,
        restaurant
    ):

        self.restaurants[
            restaurant.restaurant_id
        ] = restaurant

    def add_customer(
        self,
        customer
    ):

        self.customers[
            customer.customer_id
        ] = customer

    def add_rider(
        self,
        rider
    ):

        self.riders[
            rider.rider_id
        ] = rider

    def find_nearest_rider(
        self,
        location
    ):

        available_riders = [
            rider
            for rider in self.riders.values()
            if rider.available
        ]

        if not available_riders:
            return None

        return min(
            available_riders,
            key=lambda rider:
                rider.distance_from(location)
        )

    def create_order(
        self,
        customer_id,
        restaurant_id
    ):

        customer = self.customers.get(
            customer_id
        )

        restaurant = self.restaurants.get(
            restaurant_id
        )

        if customer is None:
            raise ValueError(
                "Customer not found"
            )

        if restaurant is None:
            raise ValueError(
                "Restaurant not found"
            )

        order = Order(
            customer,
            restaurant
        )

        self.orders[
            order.order_id
        ] = order

        return order

    def assign_rider(
        self,
        order_id
    ):

        order = self.orders.get(
            order_id
        )

        if order is None:
            raise ValueError(
                "Order not found"
            )

        rider = self.find_nearest_rider(
            order.restaurant.location
        )

        if rider is None:
            raise ValueError(
                "No rider available"
            )

        order.assign_rider(
            rider
        )

        print(
            f"Rider {rider.name} assigned "
            f"to order #{order.order_id}"
        )


# =========================================
# REAL-LIFE USAGE
# =========================================

system = DeliverySystem()


restaurant_location = Location(
    28.4595,
    77.0266
)

customer_location = Location(
    28.4740,
    77.0360
)

rider_location_1 = Location(
    28.4610,
    77.0280
)

rider_location_2 = Location(
    28.4900,
    77.0500
)


restaurant = Restaurant(
    101,
    "Food Corner",
    restaurant_location
)

restaurant.add_food(
    1,
    "Paneer Roll",
    180
)

restaurant.add_food(
    2,
    "Biryani",
    250
)

restaurant.add_food(
    3,
    "Cold Coffee",
    120
)


customer = Customer(
    501,
    "Rishav",
    customer_location
)


rider1 = Rider(
    601,
    "Amit",
    rider_location_1
)

rider2 = Rider(
    602,
    "Rahul",
    rider_location_2
)


system.add_restaurant(
    restaurant
)

system.add_customer(
    customer
)

system.add_rider(
    rider1
)

system.add_rider(
    rider2
)


order = system.create_order(
    501,
    101
)


order.add_item(
    restaurant.get_food(1),
    2
)

order.add_item(
    restaurant.get_food(2),
    1
)

order.add_item(
    restaurant.get_food(3),
    1
)


order.confirm()

order.print_invoice()


system.assign_rider(
    order.order_id
)


order.print_invoice()


order.deliver()


order.print_invoice()


print(
    "\n===== RIDER DETAILS ====="
)

print(
    rider1.name,
    rider1.total_deliveries,
    rider1.total_earnings
)

print(
    rider2.name,
    rider2.total_deliveries,
    rider2.total_earnings
)