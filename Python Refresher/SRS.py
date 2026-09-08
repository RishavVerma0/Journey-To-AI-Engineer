class Student:
    def __init__(self, name, marks):
        self.name = name
        self.__marks = marks

    @property
    def marks(self):
        return self.__marks

    @marks.setter
    def marks(self, value):
        if 0 <= value <= 100:
            self.__marks = value
        else:
            raise ValueError("Marks must be between 0 and 100")

    def grade(self):
        if self.marks >= 90:
            return "A"
        elif self.marks >= 75:
            return "B"
        elif self.marks >= 60:
            return "C"
        elif self.marks >= 40:
            return "D"
        return "F"


class GraduateStudent(Student):
    def grade(self):
        if self.marks >= 85:
            return "A"
        elif self.marks >= 70:
            return "B"
        elif self.marks >= 55:
            return "C"
        elif self.marks >= 40:
            return "D"
        return "F"


students = [
    Student("Rishav", 82),
    GraduateStudent("Aman", 82),
    Student("Rahul", 35)
]

for student in students:
    print(
        f"{student.name}: "
        f"{student.marks} → Grade {student.grade()}"
    )

students[0].marks = 95
print("\nUpdated:", students[0].name, students[0].grade())