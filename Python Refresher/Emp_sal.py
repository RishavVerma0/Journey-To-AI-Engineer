class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def calculate_bonus(self):
        return self.salary * 0.05


class Developer(Employee):
    def calculate_bonus(self):
        return self.salary * 0.10


class Manager(Employee):
    def calculate_bonus(self):
        return self.salary * 0.15


employees = [
    Developer("Aman", 60000),
    Manager("Priya", 80000),
    Employee("Rahul", 50000)
]

for employee in employees:
    bonus = employee.calculate_bonus()
    print(
        employee.name,
        "-> Bonus:",
        bonus
    )