class ExpenseTracker:
    def __init__(self):
        self.expenses = []

    def add_expense(self, category, amount):
        self.expenses.append({
            "category": category,
            "amount": amount
        })

    def total_expense(self):
        return sum(expense["amount"] for expense in self.expenses)

    def show_expenses(self):
        for expense in self.expenses:
            print(f"{expense['category']}: ₹{expense['amount']}")


tracker = ExpenseTracker()

tracker.add_expense("Food", 250)
tracker.add_expense("Travel", 500)
tracker.add_expense("Shopping", 1200)

tracker.show_expenses()

print("Total Expense:", tracker.total_expense())