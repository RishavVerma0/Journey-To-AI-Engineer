employees = [
    {
        "name": "Aarav",
        "department": "Data",
        "scores": [85, 90, 78],
        "projects": 4
    },
    {
        "name": "Priya",
        "department": "Data",
        "scores": [72, 68, 75],
        "projects": 3
    },
    {
        "name": "Rohan",
        "department": "Backend",
        "scores": [45, 52, 48],
        "projects": 2
    },
    {
        "name": "Sneha",
        "department": "AI",
        "scores": [95, 92, 97],
        "projects": 5
    },
    {
        "name": "Karan",
        "department": "Backend",
        "scores": [78, 81, 75],
        "projects": 3
    }
]


def calculate_average(scores):
    if not scores:
        return 0

    return sum(scores) / len(scores)


def get_performance(average):
    if average >= 90:
        return "Excellent"
    elif average >= 75:
        return "Good"
    elif average >= 50:
        return "Average"
    else:
        return "Poor"


def analyze_employee(employee):
    average = calculate_average(employee["scores"])

    performance = get_performance(average)

    passed = average >= 50

    return {
        "name": employee["name"],
        "department": employee["department"],
        "average": round(average, 2),
        "projects": employee["projects"],
        "performance": performance,
        "passed": passed
    }


def analyze_company(employees):

    results = []

    for employee in employees:
        result = analyze_employee(employee)
        results.append(result)

    # Find highest performer
    highest = results[0]

    for employee in results:
        if employee["average"] > highest["average"]:
            highest = employee

    # Find lowest performer
    lowest = results[0]

    for employee in results:
        if employee["average"] < lowest["average"]:
            lowest = employee

    # Calculate company average
    total_average = 0

    for employee in results:
        total_average += employee["average"]

    company_average = total_average / len(results)

    # Find passed employees
    passed_employees = []

    for employee in results:
        if employee["passed"]:
            passed_employees.append(employee["name"])

    # Find employees with 4+ projects
    high_project_employees = [
        employee["name"]
        for employee in results
        if employee["projects"] >= 4
    ]

    # Department statistics
    departments = {}

    for employee in results:

        department = employee["department"]

        if department not in departments:
            departments[department] = []

        departments[department].append(employee["average"])

    department_average = {}

    for department, scores in departments.items():
        department_average[department] = round(
            sum(scores) / len(scores),
            2
        )

    return {
        "employees": results,
        "company_average": round(company_average, 2),
        "highest_performer": highest["name"],
        "lowest_performer": lowest["name"],
        "passed_employees": passed_employees,
        "high_project_employees": high_project_employees,
        "department_average": department_average
    }


report = analyze_company(employees)

print("========== COMPANY REPORT ==========")

print(
    "Company Average:",
    report["company_average"]
)

print(
    "Highest Performer:",
    report["highest_performer"]
)

print(
    "Lowest Performer:",
    report["lowest_performer"]
)

print(
    "Passed Employees:",
    report["passed_employees"]
)

print(
    "Employees With 4+ Projects:",
    report["high_project_employees"]
)

print("\nDepartment Average:")

for department, average in report["department_average"].items():
    print(department, ":", average)

print("\nIndividual Performance:")

for employee in report["employees"]:

    print(
        employee["name"],
        "|",
        employee["department"],
        "| Average:",
        employee["average"],
        "|",
        employee["performance"]
    )