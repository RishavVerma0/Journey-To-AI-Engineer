class Employee:
   # Constructor method
    # Runs automatically when a new object is created
   def __init__(self, first, last, pay):
         self.first = first
         self.last = last
         self.email = first + '.' + last + '@example.com'
         self.pay = pay

    # self.first means:
    # get the 'first' value of the current object
   def fullname(self):
       return '{} {}'.format(self.first, self.last)

emp1 = Employee('Corey', 'Schafer', 50000)
emp2 = Employee('Test', 'User', 60000)

# emp1.first = 'Corey'
# emp1.last = 'Schafer'
# emp1.email = 'corey.schafer@example.com'
# emp1.pay = 50000

# emp2.first = 'Test'
# emp2.last = 'User'
# emp2.email = 'test.user@example.com'
# emp2.pay = 60000

# print(emp1)
# print(emp2)

# print(emp1.email)
# print(emp2.email)

print(emp1.fullname())
print(emp2.fullname())