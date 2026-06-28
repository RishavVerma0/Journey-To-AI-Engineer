class ShoppingList:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def get_all(self):
        return self.items


# Example usage
my_list = ShoppingList()
my_list.add_item("Apples")
my_list.add_item("Bananas")

print(my_list.get_all())