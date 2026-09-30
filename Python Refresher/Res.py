class Student:
    def __init__(self, name, marks):
        self.name = name
        self.marks = marks

    def calculate_result(self):
        average = sum(self.marks) / len(self.marks)

        if average >= 40:
            return "Pass"
        return "Fail"


student = Student("Rahul", [70, 65, 80, 55])

print(student.name)
print(student.calculate_result())