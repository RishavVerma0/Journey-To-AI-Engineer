class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def final_price(self):
        return self.price

    def __str__(self):
        return f"{self.name} - ₹{self.final_price():.2f}"


class DiscountProduct(Product):
    def __init__(self, name, price, discount):
        super().__init__(name, price)
        self.discount = discount

    def final_price(self):
        return self.price * (1 - self.discount / 100)


class Cart:
    def __init__(self):
        self.items = []

    def add(self, product, quantity=1):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")

        self.items.append((product, quantity))

    def remove(self, product_name):
        self.items = [
            (product, quantity)
            for product, quantity in self.items
            if product.name != product_name
        ]

    def total(self):
        return sum(
            product.final_price() * quantity
            for product, quantity in self.items
        )

    def __len__(self):
        return sum(quantity for _, quantity in self.items)

    def __iter__(self):
        return iter(self.items)

    def __str__(self):
        if not self.items:
            return "Cart is empty"

        result = ["\n--- CART ---"]

        for product, quantity in self.items:
            total = product.final_price() * quantity

            result.append(
                f"{product.name} x {quantity} = ₹{total:.2f}"
            )

        result.append(f"Total items: {len(self)}")
        result.append(f"Total price: ₹{self.total():.2f}")

        return "\n".join(result)


# Products
laptop = Product("Laptop", 60000)
phone = DiscountProduct("Phone", 30000, 10)
headphones = DiscountProduct("Headphones", 5000, 20)

# Cart
cart = Cart()

cart.add(laptop, 1)
cart.add(phone, 2)
cart.add(headphones, 3)

# Display cart
print(cart)

# Iterate over cart
print("\nIterating over cart:")

for product, quantity in cart:
    print(product, "x", quantity)