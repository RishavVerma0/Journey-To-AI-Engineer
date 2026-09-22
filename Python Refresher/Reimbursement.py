from enum import Enum
from datetime import datetime


# =========================================================
# ENUMS
# =========================================================

class ExpenseCategory(Enum):

    TRAVEL = "Travel"
    FOOD = "Food"
    HOTEL = "Hotel"
    INTERNET = "Internet"
    OFFICE = "Office"
    OTHER = "Other"


class ExpenseStatus(Enum):

    SUBMITTED = "Submitted"
    MANAGER_APPROVED = "Manager Approved"
    FINANCE_APPROVED = "Finance Approved"
    REJECTED = "Rejected"
    PAID = "Paid"


# =========================================================
# EMPLOYEE
# =========================================================

class Employee:

    def __init__(
        self,
        employee_id,
        name,
        department,
        manager=None
    ):

        self.employee_id = employee_id
        self.name = name
        self.department = department
        self.manager = manager

        self.expenses = []

    def submit_expense(self, expense):

        if expense.employee != self:

            raise ValueError(
                "Expense does not belong "
                "to this employee."
            )

        self.expenses.append(expense)

    def __str__(self):

        return (
            f"{self.employee_id} | "
            f"{self.name} | "
            f"{self.department}"
        )


# =========================================================
# EXPENSE POLICY
# =========================================================

class ExpensePolicy:

    LIMITS = {

        ExpenseCategory.TRAVEL: 50000,

        ExpenseCategory.FOOD: 3000,

        ExpenseCategory.HOTEL: 10000,

        ExpenseCategory.INTERNET: 2000,

        ExpenseCategory.OFFICE: 5000,

        ExpenseCategory.OTHER: 1000
    }

    @classmethod
    def validate(cls, category, amount):

        limit = cls.LIMITS[category]

        if amount > limit:

            return False, (
                f"Amount ₹{amount} exceeds "
                f"limit of ₹{limit}"
            )

        return True, "Valid"


# =========================================================
# EXPENSE
# =========================================================

class Expense:

    counter = 1000

    def __init__(
        self,
        employee,
        category,
        amount,
        description
    ):

        Expense.counter += 1

        self.expense_id = (
            f"EXP{Expense.counter}"
        )

        self.employee = employee
        self.category = category
        self.amount = amount
        self.description = description

        self.status = ExpenseStatus.SUBMITTED

        self.created_at = datetime.now()

        self.manager_comment = None
        self.finance_comment = None
        self.rejection_reason = None

        self.payment_reference = None

    # -----------------------------------------------------
    # MANAGER APPROVAL
    # -----------------------------------------------------

    def manager_approve(self, comment=""):

        if self.status != ExpenseStatus.SUBMITTED:

            raise Exception(
                "Expense is not awaiting "
                "manager approval."
            )

        valid, message = ExpensePolicy.validate(
            self.category,
            self.amount
        )

        if not valid:

            self.reject(message)

            return

        self.manager_comment = comment

        self.status = (
            ExpenseStatus.MANAGER_APPROVED
        )

    # -----------------------------------------------------
    # FINANCE APPROVAL
    # -----------------------------------------------------

    def finance_approve(self, comment=""):

        if self.status != (
            ExpenseStatus.MANAGER_APPROVED
        ):

            raise Exception(
                "Manager approval required "
                "before finance approval."
            )

        self.finance_comment = comment

        self.status = (
            ExpenseStatus.FINANCE_APPROVED
        )

    # -----------------------------------------------------
    # REJECT
    # -----------------------------------------------------

    def reject(self, reason):

        self.status = ExpenseStatus.REJECTED

        self.rejection_reason = reason

    # -----------------------------------------------------
    # PAYMENT
    # -----------------------------------------------------

    def mark_paid(self, payment_reference):

        if self.status != (
            ExpenseStatus.FINANCE_APPROVED
        ):

            raise Exception(
                "Finance approval required "
                "before payment."
            )

        self.payment_reference = (
            payment_reference
        )

        self.status = ExpenseStatus.PAID

    # -----------------------------------------------------
    # DISPLAY
    # -----------------------------------------------------

    def display(self):

        print("\n" + "=" * 60)

        print(
            f"Expense ID  : {self.expense_id}"
        )

        print(
            f"Employee    : "
            f"{self.employee.name}"
        )

        print(
            f"Category    : "
            f"{self.category.value}"
        )

        print(
            f"Amount      : ₹{self.amount}"
        )

        print(
            f"Description : "
            f"{self.description}"
        )

        print(
            f"Status      : "
            f"{self.status.value}"
        )

        if self.manager_comment:

            print(
                f"Manager     : "
                f"{self.manager_comment}"
            )

        if self.finance_comment:

            print(
                f"Finance     : "
                f"{self.finance_comment}"
            )

        if self.rejection_reason:

            print(
                f"Rejected    : "
                f"{self.rejection_reason}"
            )

        if self.payment_reference:

            print(
                f"Payment Ref : "
                f"{self.payment_reference}"
            )

        print("=" * 60)


# =========================================================
# FINANCE DEPARTMENT
# =========================================================

class FinanceDepartment:

    def __init__(self):

        self.expenses = []

    # -----------------------------------------------------
    # RECEIVE EXPENSE
    # -----------------------------------------------------

    def receive(self, expense):

        self.expenses.append(expense)

    # -----------------------------------------------------
    # APPROVE ALL VALID EXPENSES
    # -----------------------------------------------------

    def process_pending(self):

        for expense in self.expenses:

            if expense.status == (
                ExpenseStatus.MANAGER_APPROVED
            ):

                expense.finance_approve(
                    "Verified by Finance"
                )

    # -----------------------------------------------------
    # PAY
    # -----------------------------------------------------

    def process_payments(self):

        payment_counter = 5000

        for expense in self.expenses:

            if expense.status == (
                ExpenseStatus.FINANCE_APPROVED
            ):

                payment_counter += 1

                reference = (
                    f"PAY{payment_counter}"
                )

                expense.mark_paid(
                    reference
                )

    # -----------------------------------------------------
    # REPORT
    # -----------------------------------------------------

    def generate_report(self):

        total_submitted = 0
        total_paid = 0

        for expense in self.expenses:

            total_submitted += expense.amount

            if expense.status == ExpenseStatus.PAID:

                total_paid += expense.amount

        print("\nFINANCE REPORT")

        print(
            "Total Submitted:",
            total_submitted
        )

        print(
            "Total Paid:",
            total_paid
        )


# =========================================================
# DEMO
# =========================================================

manager = Employee(
    "M101",
    "Amit",
    "Engineering"
)

employee = Employee(
    "E101",
    "Rishav",
    "Engineering",
    manager
)

finance = FinanceDepartment()


# ---------------------------------------------------------
# EXPENSE 1
# ---------------------------------------------------------

expense1 = Expense(
    employee,
    ExpenseCategory.TRAVEL,
    18000,
    "Flight tickets for client meeting"
)

employee.submit_expense(expense1)

expense1.display()


# ---------------------------------------------------------
# MANAGER APPROVAL
# ---------------------------------------------------------

expense1.manager_approve(
    "Business travel approved."
)

expense1.display()


# ---------------------------------------------------------
# SEND TO FINANCE
# ---------------------------------------------------------

finance.receive(expense1)

finance.process_pending()

expense1.display()


# ---------------------------------------------------------
# PAYMENT
# ---------------------------------------------------------

finance.process_payments()

expense1.display()


# ---------------------------------------------------------
# EXPENSE 2 - POLICY VIOLATION
# ---------------------------------------------------------

expense2 = Expense(
    employee,
    ExpenseCategory.FOOD,
    7500,
    "Team dinner"
)

employee.submit_expense(expense2)

expense2.manager_approve(
    "Please verify food expense."
)

expense2.display()


# ---------------------------------------------------------
# REPORT
# ---------------------------------------------------------

finance.generate_report()