#Inheritance - Creating Subclasses

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
  
dev1 = Employee('Corey', 'Schafer', 50000)
dev2 = Employee('Test', 'User', 60000)

print(dev1.pay)
dev1.apply_raise()
print(dev1.pay)
print(dev2.email)