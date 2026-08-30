class Employee:
    def __init__(self, employee_id, name):
        self.employee_id = employee_id
        self.name = name

    def calculate_salary(self):
        pass

    def display_info(self):
        print("-" * 40)
        print(f"Employee ID: {self.employee_id}")
        print(f"Name: {self.name}")
        print(f"Salary: ₹{self.calculate_salary()}")


class FullTimeEmployee(Employee):
    def __init__(self, employee_id, name, monthly_salary):
        super().__init__(employee_id, name)
        self.monthly_salary = monthly_salary

    def calculate_salary(self):
        return self.monthly_salary


class PartTimeEmployee(Employee):
    def __init__(self, employee_id, name, hourly_rate, hours_worked):
        super().__init__(employee_id, name)
        self.hourly_rate = hourly_rate
        self.hours_worked = hours_worked

    def calculate_salary(self):
        return self.hourly_rate * self.hours_worked


class Freelancer(Employee):
    def __init__(self, employee_id, name, project_payment):
        super().__init__(employee_id, name)
        self.project_payment = project_payment

    def calculate_salary(self):
        return self.project_payment


class PayrollSystem:
    def __init__(self):
        self.employees = {}

    def add_employee(self, employee):
        if employee.employee_id in self.employees:
            raise ValueError("Employee already exists")

        self.employees[employee.employee_id] = employee

    def display_all_employees(self):
        if not self.employees:
            print("No employees found")
            return

        for employee in self.employees.values():
            employee.display_info()

    def calculate_total_payroll(self):
        total = 0

        for employee in self.employees.values():
            total += employee.calculate_salary()

        return total

    def find_highest_paid_employee(self):
        if not self.employees:
            return None

        highest_paid = max(
            self.employees.values(),
            key=lambda employee: employee.calculate_salary()
        )

        return highest_paid


payroll = PayrollSystem()

employee1 = FullTimeEmployee(
    101,
    "Rishav",
    60000
)

employee2 = PartTimeEmployee(
    102,
    "Rahul",
    500,
    80
)

employee3 = Freelancer(
    103,
    "Priya",
    45000
)

payroll.add_employee(employee1)
payroll.add_employee(employee2)
payroll.add_employee(employee3)

payroll.display_all_employees()

print("\nTotal Payroll:", payroll.calculate_total_payroll())

highest_paid = payroll.find_highest_paid_employee()

print("\nHighest Paid Employee:")
assert highest_paid is not None
highest_paid.display_info()