# 🍔 Food Delivery System — Composition + Polymorphism

class FoodItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def get_price(self):
        return self.price


class Order:
    def __init__(self, customer):
        self.customer = customer
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def calculate_total(self):
        return sum(item.get_price() for item in self.items)

    def apply_discount(self):
        total = self.calculate_total()

        if total >= 1000:
            return total * 0.80
        elif total >= 500:
            return total * 0.90

        return total

    def display_order(self):
        print(f"Customer: {self.customer}")

        for item in self.items:
            print(f"{item.name}: ₹{item.price}")

        print(f"Final Bill: ₹{self.apply_discount():.2f}")


class DiscountedItem(FoodItem):
    def __init__(self, name, price, discount):
        super().__init__(name, price)
        self.discount = discount

    def get_price(self):
        return self.price * (1 - self.discount / 100)


order = Order("Rishav")

order.add_item(FoodItem("Burger", 250))
order.add_item(FoodItem("Pizza", 600))
order.add_item(DiscountedItem("Fries", 200, 20))

order.display_order()