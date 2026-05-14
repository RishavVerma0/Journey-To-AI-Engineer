#Inheritance - Creating Subclasses
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
  
dev1 = Employee('Corey', 'Schafer', 50000)
dev2 = Employee('Test', 'User', 60000)

# print(dev1.pay)
# dev1.apply_raise()
# print(dev1.pay)
# print(dev2.email)

class Developer(Employee):
     def __init__(self, first, last, pay, prog_lang):
          super().__init__(first, last, pay) #This will call the constructor of the parent class Employee, and it will pass the arguments first, last, and pay to it. This is how we can initialize the attributes of the parent class in the child class.
          self.prog_lang =  prog_lang #This is an additional attribute that is specific to the Developer class, it is not present in the Employee class

dev1 = Developer('Corey', 'Schafer', 50000, 'Python')
dev2 = Developer('Test', 'User', 60000, 'Java')

# print(dev1.prog_lang)
# print(dev2.email)

# # print(help(Developer)) #This will show the method resolution order of the Developer class, which is the order in which Python looks for methods in the class and its parent classes.
# print(dev1.pay)
# dev1.apply_raise()
# print(dev1.pay)

class Manager(Employee):

    def __init__(self, first, last, pay, employees=None):
        super().__init__(first, last, pay)
        if employees is None:
            self.employees = []
        else:
            self.employees = employees
    
    def add_emp(self, emp):
        if emp not in self.employees:
            self.employees.append(emp)

    def remove_emp(self, emp):
        if emp in self.employees:
            self.employees.remove(emp)      

    def print_emps(self):
        for emp in self.employees:
            print('-->', emp.fullname())

mngr_1 = Manager('Sue', 'Smith', 90000, [dev1])
print(mngr_1.email)
mngr_1.add_emp(dev2)
mngr_1.print_emps()
mngr_1.remove_emp(dev1)
print("List after Removal")
mngr_1.print_emps()

#Checking for the Subclass and Instance
print(isinstance(Manager, Developer)) #This will return True, because Manager is an instance of the Manager class

print(issubclass(Developer, Employee)) #This will return True, because Developer is a subclass of the Employee class