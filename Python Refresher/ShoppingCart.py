# 🛒 Shopping Cart — Composition + Encapsulation


class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def total_price(self):
        return self.price * self.quantity


class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_product(self, product):
        self.items.append(product)

    def remove_product(self, product_name):
        self.items = [
            item for item in self.items
            if item.name != product_name
        ]

    def calculate_total(self):
        total = 0

        for item in self.items:
            total += item.total_price()

        return total

    def display_cart(self):
        for item in self.items:
            print(
                f"{item.name} - "
                f"₹{item.price} × {item.quantity} = "
                f"₹{item.total_price()}"
            )

        print(f"Total: ₹{self.calculate_total()}")


cart = ShoppingCart()

cart.add_product(Product("Laptop", 60000, 1))
cart.add_product(Product("Mouse", 1200, 2))
cart.add_product(Product("Keyboard", 2500, 1))

cart.display_cart()

cart.remove_product("Mouse")

print("\nAfter removing Mouse:")
cart.display_cart()