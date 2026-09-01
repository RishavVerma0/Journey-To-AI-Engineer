class Product:
    def __init__(self, product_id, name, category, price, stock):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.stock = stock

    def sell(self, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")

        if quantity > self.stock:
            raise ValueError(
                f"Not enough stock. Available: {self.stock}"
            )

        self.stock -= quantity

    def restock(self, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")

        self.stock += quantity

    def inventory_value(self):
        return self.price * self.stock

    def display(self):
        print("-" * 45)
        print(f"ID       : {self.product_id}")
        print(f"Name     : {self.name}")
        print(f"Category : {self.category}")
        print(f"Price    : ₹{self.price}")
        print(f"Stock    : {self.stock}")


class Inventory:
    def __init__(self):
        self.products = {}

    def add_product(self, product):
        if product.product_id in self.products:
            raise ValueError("Product already exists")

        self.products[product.product_id] = product

    def sell_product(self, product_id, quantity):
        product = self.products.get(product_id)

        if product is None:
            raise ValueError("Product not found")

        product.sell(quantity)

    def restock_product(self, product_id, quantity):
        product = self.products.get(product_id)

        if product is None:
            raise ValueError("Product not found")

        product.restock(quantity)

    def search(self, keyword):
        results = []

        for product in self.products.values():
            if (
                keyword.lower() in product.name.lower()
                or keyword.lower() in product.category.lower()
            ):
                results.append(product)

        return results

    def low_stock_products(self, threshold=5):
        return [
            product
            for product in self.products.values()
            if product.stock <= threshold
        ]

    def total_inventory_value(self):
        return sum(
            product.inventory_value()
            for product in self.products.values()
        )

    def sort_by_price(self, reverse=False):
        return sorted(
            self.products.values(),
            key=lambda product: product.price,
            reverse=reverse
        )

    def category_report(self):
        report = {}

        for product in self.products.values():
            category = product.category

            if category not in report:
                report[category] = {
                    "products": 0,
                    "stock": 0,
                    "value": 0
                }

            report[category]["products"] += 1
            report[category]["stock"] += product.stock
            report[category]["value"] += product.inventory_value()

        return report


inventory = Inventory()

products = [
    Product(101, "Laptop", "Electronics", 60000, 10),
    Product(102, "Mouse", "Electronics", 1200, 25),
    Product(103, "Keyboard", "Electronics", 2500, 4),
    Product(104, "Chair", "Furniture", 7000, 8),
    Product(105, "Desk", "Furniture", 12000, 3),
    Product(106, "Notebook", "Stationery", 100, 50),
]

for product in products:
    inventory.add_product(product)


try:
    inventory.sell_product(101, 2)
    inventory.sell_product(103, 2)

    inventory.restock_product(105, 10)

except ValueError as error:
    print("Error:", error)


print("\nALL PRODUCTS")

for product in inventory.products.values():
    product.display()


print("\nLOW STOCK PRODUCTS")

for product in inventory.low_stock_products():
    product.display()


print("\nMOST EXPENSIVE PRODUCTS")

for product in inventory.sort_by_price(reverse=True):
    product.display()


print("\nSEARCH: ELECTRONICS")

for product in inventory.search("Electronics"):
    product.display()


print("\nTOTAL INVENTORY VALUE")
print("₹", inventory.total_inventory_value())


print("\nCATEGORY REPORT")

report = inventory.category_report()

for category, data in report.items():
    print(
        f"{category}: "
        f"{data['products']} products | "
        f"{data['stock']} units | "
        f"₹{data['value']}"
    )