class Delivery:
    valid_states = ["Pending", "Shipped", "Out for Delivery", "Delivered"]

    def __init__(self, order_id):
        self.order_id = order_id
        self.state = "Pending"

    def update_status(self):
        current = self.valid_states.index(self.state)

        if current < len(self.valid_states) - 1:
            self.state = self.valid_states[current + 1]
        else:
            print("Order already delivered")
            return

        print(f"Order {self.order_id}: {self.state}")


class ExpressDelivery(Delivery):
    valid_states = [
        "Pending",
        "Shipped",
        "Out for Delivery",
        "Delivered"
    ]

    def update_status(self):
        if self.state == "Pending":
            self.state = "Shipped"
        elif self.state == "Shipped":
            self.state = "Out for Delivery"
        elif self.state == "Out for Delivery":
            self.state = "Delivered"
        else:
            print("Order already delivered")
            return

        print(f"Express #{self.order_id}: {self.state}")


class DeliveryManager:
    def __init__(self):
        self.deliveries = []

    def add_delivery(self, delivery):
        self.deliveries.append(delivery)

    def update_all(self):
        for delivery in self.deliveries:
            delivery.update_status()


manager = DeliveryManager()

manager.add_delivery(Delivery("ORD101"))
manager.add_delivery(ExpressDelivery("ORD102"))

for _ in range(3):
    print("\nUpdating deliveries...")
    manager.update_all()