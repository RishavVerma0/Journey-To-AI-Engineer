class Product:
    def __init__(self, product_id, name, price, stock):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock

    def reduce_stock(self, quantity):
        if quantity > self.stock:
            raise ValueError(
                f"Only {self.stock} items available"
            )

        self.stock -= quantity

    def increase_stock(self, quantity):
        self.stock += quantity

    def display_product(self):
        print("-" * 40)
        print(f"ID: {self.product_id}")
        print(f"Name: {self.name}")
        print(f"Price: ₹{self.price}")
        print(f"Stock: {self.stock}")


class ShoppingCart:
    def __init__(self):
        self.items = {}

    def add_product(self, product, quantity):
        if quantity <= 0:
            raise ValueError(
                "Quantity must be greater than zero"
            )

        if product.product_id in self.items:
            self.items[product.product_id]["quantity"] += quantity
        else:
            self.items[product.product_id] = {
                "product": product,
                "quantity": quantity
            }

    def remove_product(self, product_id):
        if product_id not in self.items:
            raise ValueError("Product not found in cart")

        del self.items[product_id]

    def calculate_total(self):
        total = 0

        for item in self.items.values():
            product = item["product"]
            quantity = item["quantity"]

            total += product.price * quantity

        return total

    def display_cart(self):
        print("\nSHOPPING CART")
        print("=" * 50)

        if not self.items:
            print("Cart is empty.")
            return

        for item in self.items.values():
            product = item["product"]
            quantity = item["quantity"]

            print(
                f"{product.name} | "
                f"₹{product.price} x {quantity} = "
                f"₹{product.price * quantity}"
            )

        print("-" * 50)
        print(f"Total: ₹{self.calculate_total()}")


class Store:
    def __init__(self):
        self.products = {}

    def add_product(self, product):
        self.products[product.product_id] = product

    def show_products(self):
        print("\nAVAILABLE PRODUCTS")
        print("=" * 50)

        for product in self.products.values():
            product.display_product()

    def get_product(self, product_id):
        return self.products.get(product_id)


class Order:
    def __init__(self, cart):
        self.cart = cart
        self.discount_percent = 0

    def apply_discount(self, discount_percent):
        if discount_percent < 0 or discount_percent > 100:
            raise ValueError("Invalid discount")

        self.discount_percent = discount_percent

    def checkout(self):
        total = self.cart.calculate_total()

        discount_amount = (
            total * self.discount_percent / 100
        )

        final_amount = total - discount_amount

        print("\nORDER SUMMARY")
        print("=" * 50)

        self.cart.display_cart()

        print(f"Discount: {self.discount_percent}%")
        print(f"Discount Amount: ₹{discount_amount}")
        print(f"Final Amount: ₹{final_amount}")

        return final_amount


store = Store()

product1 = Product(1, "Laptop", 50000, 5)
product2 = Product(2, "Mouse", 1000, 20)
product3 = Product(3, "Keyboard", 2500, 10)
product4 = Product(4, "Headphones", 3000, 8)

store.add_product(product1)
store.add_product(product2)
store.add_product(product3)
store.add_product(product4)

store.show_products()

cart = ShoppingCart()

try:
    cart.add_product(product1, 1)
    cart.add_product(product2, 2)
    cart.add_product(product3, 1)

except ValueError as error:
    print(error)

cart.display_cart()

order = Order(cart)

order.apply_discount(10)

order.checkout()