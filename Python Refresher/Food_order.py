class FoodOrder:
    def __init__(self):
        self.items = []

    def add_item(self, name, price, quantity):
        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def calculate_total(self):
        total = 0

        for item in self.items:
            total += item["price"] * item["quantity"]

        return total

    def show_order(self):
        for item in self.items:
            print(
                f"{item['name']} x {item['quantity']} "
                f"= ₹{item['price'] * item['quantity']}"
            )

        print("Total: ₹", self.calculate_total())


order = FoodOrder()

order.add_item("Paneer Tikka", 250, 2)
order.add_item("Butter Naan", 60, 3)
order.add_item("Coke", 50, 2)

order.show_order()