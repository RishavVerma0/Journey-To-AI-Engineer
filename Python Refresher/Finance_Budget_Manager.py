class BudgetManager:
    def __init__(self, monthly_budget):
        self.monthly_budget = monthly_budget
        self.expenses = []

    def add_expense(self, category, amount):
        if amount <= 0:
            print("Amount must be greater than zero.")
            return

        self.expenses.append({
            "category": category,
            "amount": amount
        })

        print(f"Added ₹{amount} for {category}")

    def total_spent(self):
        return sum(expense["amount"] for expense in self.expenses)

    def remaining_budget(self):
        return self.monthly_budget - self.total_spent()

    def category_summary(self):
        summary = {}

        for expense in self.expenses:
            category = expense["category"]
            summary[category] = (
                summary.get(category, 0) + expense["amount"]
            )

        return summary

    def show_report(self):
        print(f"\nMonthly Budget: ₹{self.monthly_budget}")
        print(f"Total Spent: ₹{self.total_spent()}")
        print(f"Remaining: ₹{self.remaining_budget()}")

        print("\nCategory Breakdown:")
        for category, amount in self.category_summary().items():
            print(f"{category}: ₹{amount}")

        if self.remaining_budget() < 0:
            print("Warning: Budget exceeded!")


budget = BudgetManager(15000)

budget.add_expense("Food", 3500)
budget.add_expense("Travel", 2000)
budget.add_expense("Shopping", 4500)
budget.add_expense("Food", 1200)
budget.add_expense("Bills", 3000)

budget.show_report()