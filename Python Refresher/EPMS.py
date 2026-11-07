class Employee:

    def __init__(self, name, employee_id, salary):
        self.name = name
        self.employee_id = employee_id
        self.__salary = salary

    def get_salary(self):
        return self.__salary

    def calculate_bonus(self):
        return self.__salary * 0.10

    def display_details(self):
        print(f"Name: {self.name}")
        print(f"Employee ID: {self.employee_id}")
        print(f"Salary: ₹{self.__salary}")
        print(f"Bonus: ₹{self.calculate_bonus():.2f}")


class Developer(Employee):

    def __init__(self, name, employee_id, salary, programming_language):
        super().__init__(name, employee_id, salary)
        self.programming_language = programming_language

    # Method overriding
    def calculate_bonus(self):
        return self.get_salary() * 0.20

    def display_details(self):
        super().display_details()
        print(f"Programming Language: {self.programming_language}")


class Manager(Employee):

    def calculate_bonus(self):
        return self.get_salary() * 0.30


# Creating objects
developer = Developer("Rishav", 101, 60000, "Python")
manager = Manager("Rahul", 102, 90000)

# Display employee information
print("----- Developer Details -----")
developer.display_details()

print("\n----- Manager Details -----")
manager.display_details()