#Special (Magic/Dunder) Methods
class Employee:

    raise_amt = 1.04

    def __init__(self, first, last, pay) :
        self.first = first
        self.last = last
        self.email = first + '.' + last + '@email.com'
        self.pay = pay

    def fullname (self) :
        return "{} {}". format(self. first, self. last)
    
    def apply_raise(self):
        self.pay = int(self. pay * self. raise_amt)

    def __repr__ (self):
        return "Employee('{}', '{}', {}')" .format(self.first, self.last, self.pay)

    def __str__(self):
        return '{} - {}'.format(self.fullname(), self.email)
    
emp_1 = Employee('Corey', 'Schafer', 50000)
emp_2 = Employee('Test', 'Employee', 60000)

# print(emp_1)
# print(emp_2)

print(repr(emp_1))
print(str(emp_1))
print(repr(emp_2))
print(str(emp_2))

print(int.__add__(10,20)) #This will add 10 and 20, and it will use the __add__ method of the int class to do it    
print(str.__add__('Rishav', ' ', 'Verma')) #This will concatenate the two strings, and it will use the __add__ method of the str class to do it  