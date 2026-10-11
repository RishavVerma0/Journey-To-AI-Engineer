class AttendanceSystem:
    def __init__(self):
        self.employees = {}

    def add_employee(self, employee_id, name):
        self.employees[employee_id] = {
            "name": name,
            "attendance": []
        }

    def mark_attendance(self, employee_id, status):
        if employee_id not in self.employees:
            print("Employee not found")
            return

        if status not in ["Present", "Absent"]:
            print("Invalid attendance status")
            return

        self.employees[employee_id]["attendance"].append(status)

    def calculate_attendance(self, employee_id):
        employee = self.employees[employee_id]
        records = employee["attendance"]

        total_days = len(records)
        present_days = records.count("Present")

        percentage = (
            (present_days / total_days) * 100
            if total_days else 0
        )

        print(f"Employee: {employee['name']}")
        print(f"Present Days: {present_days}/{total_days}")
        print(f"Attendance: {percentage:.1f}%")


system = AttendanceSystem()

system.add_employee(101, "Rahul")
system.add_employee(102, "Priya")

system.mark_attendance(101, "Present")
system.mark_attendance(101, "Present")
system.mark_attendance(101, "Absent")
system.mark_attendance(101, "Present")

system.calculate_attendance(101)