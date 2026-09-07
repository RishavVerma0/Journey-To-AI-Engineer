class Product:
    def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock

    def reduce_stock(self, quantity):
        if quantity > self.stock:
            return False

        self.stock -= quantity
        return True


class OrderItem:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

    def total_price(self):
        return self.product.price * self.quantity


class Order:
    order_count = 0

    def __init__(self):
        Order.order_count += 1
        self.order_id = Order.order_count
        self.items = []
        self.status = "Pending"

    def add_item(self, product, quantity):
        if product.reduce_stock(quantity):
            self.items.append(OrderItem(product, quantity))
            print(f"{product.name} added to order")
        else:
            print(f"Not enough stock for {product.name}")

    def calculate_total(self):
        return sum(item.total_price() for item in self.items)

    def place_order(self):
        if not self.items:
            print("Order is empty")
            return

        self.status = "Confirmed"
        print(f"Order #{self.order_id} confirmed")

    def display_order(self):
        print(f"\nOrder ID: {self.order_id}")
        print(f"Status: {self.status}")

        for item in self.items:
            print(
                f"{item.product.name} × {item.quantity} "
                f"= ₹{item.total_price()}"
            )

        print(f"Total: ₹{self.calculate_total()}")


laptop = Product("Laptop", 60000, 2)
mouse = Product("Mouse", 1000, 5)

order = Order()

order.add_item(laptop, 1)
order.add_item(mouse, 2)

order.place_order()
order.display_order()

print("\nRemaining stock:")
print("Laptop:", laptop.stock)
print("Mouse:", mouse.stock)