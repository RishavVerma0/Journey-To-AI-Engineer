class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return f"{self.name} - ₹{self.price}"


class Cart:
    def __init__(self):
        self.items = []

    def add_product(self, product):
        self.items.append(product)

    def remove_product(self, product_name):
        self.items = [
            item for item in self.items
            if item.name != product_name
        ]

    def total_price(self):
        return sum(item.price for item in self.items)

    def show_cart(self):
        for item in self.items:
            print(item)

        print("Total:", self.total_price())


cart = Cart()

cart.add_product(Product("Keyboard", 1500))
cart.add_product(Product("Mouse", 800))
cart.add_product(Product("Headphones", 2500))

cart.remove_product("Mouse")

cart.show_cart()