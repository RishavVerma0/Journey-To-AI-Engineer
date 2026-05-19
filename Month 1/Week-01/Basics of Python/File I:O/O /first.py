# Python provides built-in support for handling files through the open() function and file objects.

# ⸻

# 1. What is File I/O?

# * Input → Reading data from a file
# * Output → Writing data to a file

# Common file types:

# * Text files (.txt, .csv, .json)
# * Binary files (.jpg, .pdf, .mp3)

def add_student():
    name = input("Enter name: ")
    marks = input("Enter marks: ")

    with open("students.txt", "a") as f:
        f.write(f"{name},{marks}\n")


def view_students():
    with open("students.txt", "r") as f:
        for line in f:
            name, marks = line.strip().split(",")

            print("Name:", name)
            print("Marks:", marks)
            print()


while True:
    print("1. Add")
    print("2. View")
    print("3. Exit")

    choice = input("Choice: ")

    if choice == "1":
        add_student()

    elif choice == "2":
        view_students()

    elif choice == "3":
        break