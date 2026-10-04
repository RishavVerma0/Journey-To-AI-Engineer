class Inventory:
    def __init__(self):
        self.products = {}

    def add_product(self, name, quantity):
        self.products[name] = self.products.get(name, 0) + quantity

    def sell_product(self, name, quantity):
        if self.products.get(name, 0) >= quantity:
            self.products[name] -= quantity
            print(f"{quantity} {name} sold")
        else:
            print("Not enough stock")

    def show_inventory(self):
        for name, quantity in self.products.items():
            print(f"{name}: {quantity}")


inventory = Inventory()

inventory.add_product("Laptop", 5)
inventory.add_product("Mouse", 10)
inventory.add_product("Laptop", 2)

inventory.sell_product("Laptop", 3)

inventory.show_inventory()