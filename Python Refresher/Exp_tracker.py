class Expense:
    categories = {
        "food",
        "travel",
        "shopping",
        "bills"
    }

    def __init__(self, amount, category, description):
        if amount <= 0:
            raise ValueError("Amount must be positive")

        if category not in self.categories:
            raise ValueError("Invalid category")

        self.amount = amount
        self.category = category
        self.description = description

    def __str__(self):
        return (
            f"{self.category.title()} | "
            f"₹{self.amount} | "
            f"{self.description}"
        )


class ExpenseTracker:
    def __init__(self):
        self.expenses = []

    def add_expense(self, expense):
        self.expenses.append(expense)

    def total_expense(self):
        return sum(expense.amount for expense in self.expenses)

    def category_total(self, category):
        return sum(
            expense.amount
            for expense in self.expenses
            if expense.category == category
        )

    def highest_expense(self):
        if not self.expenses:
            return None

        return max(
            self.expenses,
            key=lambda expense: expense.amount
        )

    def display(self):
        for expense in self.expenses:
            print(expense)

        print(f"\nTotal: ₹{self.total_expense()}")


tracker = ExpenseTracker()

tracker.add_expense(
    Expense(250, "food", "Lunch")
)

tracker.add_expense(
    Expense(1200, "travel", "Cab")
)

tracker.add_expense(
    Expense(800, "shopping", "Shoes")
)

tracker.add_expense(
    Expense(500, "food", "Dinner")
)

tracker.display()

print("\nFood:", tracker.category_total("food"))
print("Highest:", tracker.highest_expense())