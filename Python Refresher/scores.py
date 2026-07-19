students = {
    "Alice": 85,
    "Bob": 92,
    "Charlie": 78
}

try:
    name = input("Enter student name: ")

    if name in students:
        print(f"{name}'s score: {students[name]}")
    else:
        raise KeyError("Student not found.")

except KeyError as e:
    print("Error:", e)