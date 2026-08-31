from datetime import datetime


class Expense:
    def __init__(
        self,
        expense_id,
        amount,
        category,
        description
    ):
        if amount <= 0:
            raise ValueError(
                "Expense amount must be greater than 0"
            )

        self.expense_id = expense_id
        self.amount = amount
        self.category = category
        self.description = description
        self.date = datetime.now()

    def display(self):
        print("-" * 45)
        print(f"ID: {self.expense_id}")
        print(f"Amount: ₹{self.amount}")
        print(f"Category: {self.category}")
        print(f"Description: {self.description}")
        print(
            f"Date: "
            f"{self.date.strftime('%Y-%m-%d')}"
        )


class ExpenseTracker:
    def __init__(self):
        self.expenses = {}

    def add_expense(self, expense):
        if expense.expense_id in self.expenses:
            raise ValueError(
                "Expense ID already exists"
            )

        self.expenses[expense.expense_id] = expense

        print("Expense added successfully")

    def delete_expense(self, expense_id):
        if expense_id not in self.expenses:
            raise ValueError("Expense not found")

        del self.expenses[expense_id]

        print("Expense deleted successfully")

    def display_all_expenses(self):
        if not self.expenses:
            print("No expenses found")
            return

        print("\nALL EXPENSES")

        for expense in self.expenses.values():
            expense.display()

    def calculate_total_expense(self):
        total = 0

        for expense in self.expenses.values():
            total += expense.amount

        return total

    def filter_by_category(self, category):
        filtered_expenses = []

        for expense in self.expenses.values():
            if expense.category.lower() == category.lower():
                filtered_expenses.append(expense)

        return filtered_expenses

    def find_highest_expense(self):
        if not self.expenses:
            return None

        return max(
            self.expenses.values(),
            key=lambda expense: expense.amount
        )

    def category_summary(self):
        summary = {}

        for expense in self.expenses.values():
            category = expense.category

            if category not in summary:
                summary[category] = 0

            summary[category] += expense.amount

        return summary

    def display_category_summary(self):
        summary = self.category_summary()

        print("\nCATEGORY SUMMARY")
        print("=" * 40)

        for category, amount in summary.items():
            print(f"{category}: ₹{amount}")

    def monthly_summary(self):
        summary = {}

        for expense in self.expenses.values():
            month = expense.date.strftime("%B %Y")

            if month not in summary:
                summary[month] = 0

            summary[month] += expense.amount

        return summary


tracker = ExpenseTracker()

expense1 = Expense(
    1,
    500,
    "Food",
    "Dinner with friends"
)

expense2 = Expense(
    2,
    1200,
    "Travel",
    "Cab booking"
)

expense3 = Expense(
    3,
    2500,
    "Shopping",
    "New shoes"
)

expense4 = Expense(
    4,
    300,
    "Food",
    "Coffee and snacks"
)

tracker.add_expense(expense1)
tracker.add_expense(expense2)
tracker.add_expense(expense3)
tracker.add_expense(expense4)

tracker.display_all_expenses()

print(
    "\nTotal Expense:",
    tracker.calculate_total_expense()
)

food_expenses = tracker.filter_by_category("Food")

print("\nFOOD EXPENSES")

for expense in food_expenses:
    expense.display()

highest = tracker.find_highest_expense()

print("\nHIGHEST EXPENSE")
assert highest is not None
highest.display()

tracker.display_category_summary()

print("\nMONTHLY SUMMARY")

monthly_data = tracker.monthly_summary()

for month, amount in monthly_data.items():
    print(f"{month}: ₹{amount}")