students = [
    {"name": "Alice", "age": 23},
    {"name": "Bob", "age": 19},
    {"name": "Charlie", "age": 21}
]

# Sort by age
sorted_students = sorted(students, key=lambda student: student["age"])

#Sort in descending order:

print(sorted_students)

sorted_students = sorted(
    students,
    key=lambda student: student["age"],
    reverse=True
)

print(sorted_students)