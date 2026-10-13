class OrderManager:
    def __init__(self):
        self.orders = {}
        self.next_order_id = 1001

    def create_order(self, customer, items):
        order_id = self.next_order_id
        total = sum(item["price"] * item["quantity"] for item in items)

        self.orders[order_id] = {
            "customer": customer,
            "items": items,
            "total": total,
            "status": "Pending"
        }

        self.next_order_id += 1
        print(f"Order #{order_id} created for ₹{total}")
        return order_id

    def update_status(self, order_id, status):
        order = self.orders.get(order_id)

        if not order:
            print("Order not found")
            return

        if order["status"] in ["Delivered", "Cancelled"]:
            print("Order cannot be updated")
            return

        if status not in ["Confirmed", "Shipped", "Delivered", "Cancelled"]:
            print("Invalid status")
            return

        order["status"] = status
        print(f"Order #{order_id}: {status}")

    def show_order(self, order_id):
        order = self.orders.get(order_id)

        if not order:
            print("Order not found")
            return

        print(f"\nCustomer: {order['customer']}")
        print(f"Total: ₹{order['total']}")
        print(f"Status: {order['status']}")

        for item in order["items"]:
            print(f"{item['name']} x {item['quantity']}")


manager = OrderManager()

order_id = manager.create_order(
    "Rahul",
    [
        {"name": "Laptop", "price": 50000, "quantity": 1},
        {"name": "Mouse", "price": 800, "quantity": 2},
        {"name": "Keyboard", "price": 1500, "quantity": 1}
    ]
)

manager.update_status(order_id, "Confirmed")
manager.update_status(order_id, "Shipped")
manager.show_order(order_id)