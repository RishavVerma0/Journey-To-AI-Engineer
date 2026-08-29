class Student:
    def __init__(self, student_id, name, age):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.marks = []

    def add_mark(self, mark):
        if 0 <= mark <= 100:
            self.marks.append(mark)
        else:
            raise ValueError("Marks must be between 0 and 100")

    def calculate_average(self):
        if not self.marks:
            return 0

        return sum(self.marks) / len(self.marks)

    def get_grade(self):
        average = self.calculate_average()

        if average >= 90:
            return "A"
        elif average >= 75:
            return "B"
        elif average >= 60:
            return "C"
        elif average >= 40:
            return "D"
        else:
            return "F"

    def display_info(self):
        print("-" * 40)
        print(f"ID: {self.student_id}")
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
        print(f"Marks: {self.marks}")
        print(f"Average: {self.calculate_average():.2f}")
        print(f"Grade: {self.get_grade()}")


class StudentManagementSystem:
    def __init__(self):
        self.students = {}

    def add_student(self, student):
        if student.student_id in self.students:
            print("Student ID already exists.")
        else:
            self.students[student.student_id] = student
            print("Student added successfully.")

    def add_marks(self, student_id, mark):
        if student_id not in self.students:
            print("Student not found.")
            return

        try:
            self.students[student_id].add_mark(mark)
            print("Mark added successfully.")
        except ValueError as error:
            print(error)

    def display_all_students(self):
        if not self.students:
            print("No students available.")
            return

        for student in self.students.values():
            student.display_info()

    def find_topper(self):
        if not self.students:
            print("No students available.")
            return

        topper = max(
            self.students.values(),
            key=lambda student: student.calculate_average()
        )

        print("\nTOPPER")
        topper.display_info()

    def search_student(self, name):
        found_students = []

        for student in self.students.values():
            if name.lower() in student.name.lower():
                found_students.append(student)

        if not found_students:
            print("No student found.")
        else:
            for student in found_students:
                student.display_info()


system = StudentManagementSystem()

student1 = Student(101, "Rishav", 23)
student1.add_mark(85)
student1.add_mark(92)
student1.add_mark(78)

student2 = Student(102, "Rahul", 22)
student2.add_mark(70)
student2.add_mark(88)
student2.add_mark(91)

student3 = Student(103, "Priya", 21)
student3.add_mark(95)
student3.add_mark(90)
student3.add_mark(98)

system.add_student(student1)
system.add_student(student2)
system.add_student(student3)

system.add_marks(101, 88)

system.display_all_students()

system.find_topper()

system.search_student("ri")