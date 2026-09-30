class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, name, price):
        self.items.append((name, price))

    def total(self):
        return sum(price for name, price in self.items)


cart = Cart()

cart.add_item("Keyboard", 1200)
cart.add_item("Mouse", 600)
cart.add_item("USB Cable", 300)

print("Total:", cart.total())