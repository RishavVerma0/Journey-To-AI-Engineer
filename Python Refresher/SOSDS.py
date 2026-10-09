class ShoppingOrder:
    def __init__(self, customer):
        self.customer = customer
        self.items = []

    def add_item(self, name, price):
        self.items.append({"name": name, "price": price})

    def calculate_discount(self):
        total = sum(item["price"] for item in self.items)

        if total >= 5000:
            return total * 0.20
        elif total >= 2000:
            return total * 0.10
        return 0

    def generate_bill(self):
        total = sum(item["price"] for item in self.items)
        discount = self.calculate_discount()

        print(f"Customer: {self.customer}")
        for item in self.items:
            print(f"{item['name']}: ₹{item['price']}")

        print(f"Subtotal: ₹{total}")
        print(f"Discount: ₹{discount:.2f}")
        print(f"Final Amount: ₹{total - discount:.2f}")


order = ShoppingOrder("Rahul")

order.add_item("Keyboard", 1500)
order.add_item("Mouse", 800)
order.add_item("Headphones", 3000)

order.generate_bill()