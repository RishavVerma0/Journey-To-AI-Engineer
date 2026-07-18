marks = [78, 92, 65, 88, 95]

print("Marks:", marks)
print("Highest:", max(marks))
print("Lowest:", min(marks))
print("Average:", sum(marks) / len(marks))

print("\nStudents scoring 80 or above:")
for mark in marks:
    if mark >= 80:
        print(mark)