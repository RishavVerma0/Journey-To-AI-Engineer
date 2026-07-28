def calculate_grade(avg):
    if avg >= 90:
        return "A"
    elif avg >= 75:
        return "B"
    elif avg >= 60:
        return "C"
    elif avg >= 40:
        return "D"
    return "F"


def generate_report(students):
    report = []

    for name, marks in students.items():
        average = sum(marks) / len(marks)
        highest = max(marks)
        lowest = min(marks)

        report.append({
            "name": name,
            "average": average,
            "grade": calculate_grade(average),
            "highest": highest,
            "lowest": lowest
        })

    report.sort(key=lambda x: x["average"], reverse=True)

    print("\n===== REPORT CARD =====")

    for rank, student in enumerate(report, start=1):
        print(f"""
Rank: {rank}
Name: {student['name']}
Average: {student['average']:.2f}
Highest: {student['highest']}
Lowest: {student['lowest']}
Grade: {student['grade']}
""")


def main():
    students = {}

    try:
        n = int(input("Number of students: "))

        for _ in range(n):
            name = input("\nStudent Name: ")

            marks = list(map(int, input(
                "Enter 5 marks separated by space: "
            ).split()))

            if len(marks) != 5:
                raise ValueError("Exactly 5 marks required.")

            students[name] = marks

        generate_report(students)

    except ValueError as e:
        print("Error:", e)


if __name__ == "__main__":
    main()