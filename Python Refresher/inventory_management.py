class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.__price = price
        self.quantity = quantity

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if value > 0:
            self.__price = value
        else:
            raise ValueError("Price must be positive")

    def restock(self, quantity):
        if quantity > 0:
            self.quantity += quantity

    def sell(self, quantity):
        if quantity <= 0:
            return False

        if quantity > self.quantity:
            return False

        self.quantity -= quantity
        return True

    def __str__(self):
        return f"{self.name} | ₹{self.price} | Stock: {self.quantity}"

    def __len__(self):
        return self.quantity


class Inventory:
    def __init__(self):
        self.products = {}

    def add_product(self, product):
        self.products[product.name] = product

    def sell_product(self, name, quantity):
        if name not in self.products:
            print("Product not found")
            return

        product = self.products[name]

        if product.sell(quantity):
            print(f"{quantity} × {name} sold")
        else:
            print("Insufficient stock")

    def display(self):
        for product in self.products.values():
            print(product)


inventory = Inventory()

laptop = Product("Laptop", 60000, 5)
mouse = Product("Mouse", 1200, 10)

inventory.add_product(laptop)
inventory.add_product(mouse)

inventory.display()

print("\nSelling products:")
inventory.sell_product("Laptop", 2)
inventory.sell_product("Mouse", 3)

print("\nUpdated inventory:")
inventory.display()

print("\nStock using len():", len(laptop))