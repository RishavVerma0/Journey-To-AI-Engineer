class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def give_raise(self, percentage):
        self.salary += self.salary * percentage / 100

    def show_details(self):
        print(f"Employee: {self.name}")
        print(f"Salary: ₹{self.salary:.0f}")


employee = Employee("Rishav", 35000)

employee.give_raise(10)
employee.show_details()