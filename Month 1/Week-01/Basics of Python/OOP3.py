#Classmethods and staticmethods
class Employee:
   
   raise_amount = 1.04 #This is a class variable, it is shared by all instances of the class
   number_of_employees = 0 #This is a class variable, it is shared by all instances of the class
   # Constructor method
    # Runs automatically when a new object is created
   def __init__(self, first, last, pay):
         self.first = first
         self.last = last
         self.email = first + '.' + last + '@example.com'
         self.pay = pay
         Employee.number_of_employees += 1 #This will increment the number of employees every time a new employee is created    

    # self.first means:
    # get the 'first' value of the current object
   def fullname(self):
       return '{} {}'.format(self.first, self.last)
   
   #We are creating a method apply_raise that will take the current pay and multiply it by the raise amount
   def apply_raise(self):
        self.pay = int(self.pay * Employee.raise_amount) #This will give a 4% raise to the employee
        #self.pay = int(self.pay * self.raise_amount) #This will also give a 4% raise to the employee, but it will use the class variable raise_amount, which is shared by all instances of the class.
   
   @classmethod
   def set_raise_amount(cls, amount):
        cls.raise_amount = amount #This will change the raise amount for all instances of the class, because it is a class variable 

   @classmethod
   def from_string(cls, emp_str):
        firstname, lastname, pay = emp_str.split('-') #This will split the string into a list of three elements, and assign them to the variables firstname, lastname, and pay
        return cls(firstname, lastname, pay) #This will create a new employee object using the values from the string
       
   @staticmethod
   def is_workday(day):
        if day.weekday() == 5 or day.weekday() == 6: #This will check if the day is a Saturday or Sunday
            return False
        return True
   

emp1 = Employee('Corey', 'Schafer', 50000)
emp2 = Employee('Test', 'User', 60000)

#Employee.set_raise_amount(1.05) #This will change the raise amount for all instances of the class, because it is a class variable   
# emp1.set_raise_amount(1.06) #This will also change the raise amount for all instances of the class, because it is a class variable

# print(Employee.raise_amount)
# print(emp1.raise_amount)
# print(emp2.raise_amount)

# emp_str_1 = 'John-Doe-70000'
# emp_str_2 = 'Jane-Doe-80000'

# firstname, lastname, pay = emp_str_1.split('-') #This will split the string into a list of three elements, and assign them to the variables firstname, lastname, and pay
# new_emp_1 = Employee(firstname, lastname, pay) #This will create a new employee object using the values from the string

# new_emp_1 = Employee.from_string(emp_str_1) #This will create a new employee object using the values from the string, and it will use the classmethod from_string to do it
# new_emp_2 = Employee.from_string(emp_str_2) #This will create a new employee object using the values from the string, and it will use the classmethod from_string to do

# print(new_emp_1.email)
# print(new_emp_1.pay)

# print(new_emp_2.email)
# print(new_emp_2.pay)

import datetime
my_date = datetime.date(2026,4,26)
print(Employee.is_workday(my_date)) #This will check if the date is a workday or not, and it will use the staticmethod is_workday to do it