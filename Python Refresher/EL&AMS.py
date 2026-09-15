from datetime import date


class Employee:

    def __init__(
        self,
        employee_id,
        name,
        department,
        annual_leaves=24
    ):
        self.employee_id = employee_id
        self.name = name
        self.department = department

        self.annual_leaves = annual_leaves
        self.used_leaves = 0

        self.attendance = {}

    @property
    def remaining_leaves(self):

        return (
            self.annual_leaves
            - self.used_leaves
        )

    def mark_attendance(
        self,
        attendance_date,
        status
    ):

        valid_status = {
            "PRESENT",
            "ABSENT",
            "WORK_FROM_HOME"
        }

        if status not in valid_status:
            raise ValueError(
                "Invalid attendance status"
            )

        self.attendance[
            attendance_date
        ] = status

    def apply_leave(self, leave_days):

        if leave_days <= 0:
            raise ValueError(
                "Leave days must be positive"
            )

        if leave_days > self.remaining_leaves:
            raise ValueError(
                "Insufficient leave balance"
            )

        self.used_leaves += leave_days

        print(
            f"{self.name}: "
            f"{leave_days} leave(s) approved"
        )

    def attendance_summary(self):

        present = 0
        absent = 0
        wfh = 0

        for status in self.attendance.values():

            if status == "PRESENT":
                present += 1

            elif status == "ABSENT":
                absent += 1

            elif status == "WORK_FROM_HOME":
                wfh += 1

        print(
            f"\n--- {self.name} Attendance ---"
        )

        print(f"Present : {present}")
        print(f"Absent  : {absent}")
        print(f"WFH     : {wfh}")

    def show_details(self):

        print("\n==========================")
        print(f"ID       : {self.employee_id}")
        print(f"Name     : {self.name}")
        print(f"Department: {self.department}")
        print(
            f"Leave Balance: "
            f"{self.remaining_leaves}"
        )
        print("==========================")


class Manager(Employee):

    def __init__(
        self,
        employee_id,
        name,
        department
    ):

        super().__init__(
            employee_id,
            name,
            department,
            annual_leaves=30
        )

        self.team = []

    def add_employee(self, employee):

        self.team.append(employee)

    def team_report(self):

        print(
            f"\n===== {self.name}'s TEAM ====="
        )

        for employee in self.team:

            print(
                f"{employee.employee_id} | "
                f"{employee.name} | "
                f"{employee.department} | "
                f"Leaves: "
                f"{employee.remaining_leaves}"
            )

    def approve_leave(
        self,
        employee,
        leave_days
    ):

        if employee not in self.team:
            raise ValueError(
                "Employee does not belong to this team"
            )

        employee.apply_leave(
            leave_days
        )

        print(
            f"Leave approved by "
            f"{self.name}"
        )


class AttendanceSystem:

    def __init__(self):

        self.employees = {}

    def register(self, employee):

        if employee.employee_id in self.employees:
            raise ValueError(
                "Employee already registered"
            )

        self.employees[
            employee.employee_id
        ] = employee

    def mark(
        self,
        employee_id,
        attendance_date,
        status
    ):

        employee = self.get_employee(
            employee_id
        )

        employee.mark_attendance(
            attendance_date,
            status
        )

    def get_employee(self, employee_id):

        if employee_id not in self.employees:
            raise ValueError(
                "Employee not found"
            )

        return self.employees[
            employee_id
        ]

    def monthly_report(self):

        print(
            "\n========== MONTHLY REPORT =========="
        )

        for employee in self.employees.values():

            present = 0
            absent = 0
            wfh = 0

            for status in employee.attendance.values():

                if status == "PRESENT":
                    present += 1

                elif status == "ABSENT":
                    absent += 1

                elif status == "WORK_FROM_HOME":
                    wfh += 1

            print(
                f"{employee.name:15} | "
                f"P: {present} | "
                f"A: {absent} | "
                f"WFH: {wfh} | "
                f"Leaves: {employee.remaining_leaves}"
            )


# =========================================
# REAL-LIFE USAGE
# =========================================

system = AttendanceSystem()


manager = Manager(
    101,
    "Ankit",
    "Engineering"
)

employee1 = Employee(
    102,
    "Rishav",
    "Engineering"
)

employee2 = Employee(
    103,
    "Rahul",
    "Engineering"
)


system.register(manager)
system.register(employee1)
system.register(employee2)


manager.add_employee(employee1)
manager.add_employee(employee2)


# Attendance

system.mark(
    102,
    date(2026, 9, 1),
    "PRESENT"
)

system.mark(
    102,
    date(2026, 9, 2),
    "WORK_FROM_HOME"
)

system.mark(
    102,
    date(2026, 9, 3),
    "PRESENT"
)

system.mark(
    103,
    date(2026, 9, 1),
    "ABSENT"
)

system.mark(
    103,
    date(2026, 9, 2),
    "PRESENT"
)

system.mark(
    103,
    date(2026, 9, 3),
    "PRESENT"
)


# Leave approval

manager.approve_leave(
    employee1,
    2
)

manager.approve_leave(
    employee2,
    1
)


# Reports

employee1.show_details()
employee1.attendance_summary()

employee2.show_details()
employee2.attendance_summary()

manager.team_report()

system.monthly_report()