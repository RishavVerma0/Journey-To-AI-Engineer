from enum import Enum
from datetime import date, timedelta


# ============================================================
# ENUMS
# ============================================================

class LoanStatus(Enum):
    APPLICATION = "Application"
    APPROVED = "Approved"
    ACTIVE = "Active"
    COMPLETED = "Completed"
    DEFAULTED = "Defaulted"
    REJECTED = "Rejected"


class EmploymentType(Enum):
    SALARIED = "Salaried"
    SELF_EMPLOYED = "Self Employed"
    BUSINESS = "Business"


class PaymentStatus(Enum):
    PENDING = "Pending"
    PAID = "Paid"
    OVERDUE = "Overdue"


# ============================================================
# CUSTOMER
# ============================================================

class Customer:

    def __init__(
        self,
        customer_id,
        name,
        age,
        monthly_income,
        employment_type,
        credit_score
    ):
        self.customer_id = customer_id
        self.name = name
        self.age = age
        self.monthly_income = monthly_income
        self.employment_type = employment_type
        self.credit_score = credit_score

        self.loans = []

    def add_loan(self, loan):
        self.loans.append(loan)

    def active_loans(self):

        return [
            loan
            for loan in self.loans
            if loan.status == LoanStatus.ACTIVE
        ]

    def total_monthly_emi(self):

        return sum(
            loan.emi
            for loan in self.active_loans()
        )

    def debt_to_income_ratio(self):

        if self.monthly_income == 0:
            return 1

        return round(
            self.total_monthly_emi()
            / self.monthly_income,
            2
        )

    def __str__(self):

        return (
            f"{self.name} | "
            f"Income: ₹{self.monthly_income} | "
            f"Credit Score: {self.credit_score}"
        )


# ============================================================
# LOAN PRODUCT
# ============================================================

class LoanProduct:

    def __init__(
        self,
        product_id,
        name,
        min_credit_score,
        max_amount,
        annual_interest_rate,
        max_tenure_months
    ):
        self.product_id = product_id
        self.name = name
        self.min_credit_score = min_credit_score
        self.max_amount = max_amount
        self.annual_interest_rate = annual_interest_rate
        self.max_tenure_months = max_tenure_months

    def __str__(self):

        return (
            f"{self.name} | "
            f"Max: ₹{self.max_amount} | "
            f"Interest: {self.annual_interest_rate}%"
        )


# ============================================================
# REPAYMENT
# ============================================================

class Repayment:

    def __init__(
        self,
        installment_number,
        due_date,
        principal,
        interest
    ):
        self.installment_number = installment_number
        self.due_date = due_date

        self.principal = principal
        self.interest = interest

        self.amount = round(
            principal + interest,
            2
        )

        self.status = PaymentStatus.PENDING
        self.payment_date = None
        self.penalty = 0

    def pay(self, payment_date):

        if self.status == PaymentStatus.PAID:
            raise ValueError(
                "Installment already paid."
            )

        self.status = PaymentStatus.PAID
        self.payment_date = payment_date

    def check_overdue(self, today):

        if (
            self.status == PaymentStatus.PENDING
            and today > self.due_date
        ):

            self.status = PaymentStatus.OVERDUE

            overdue_days = (
                today - self.due_date
            ).days

            self.penalty = round(
                self.amount
                * 0.001
                * overdue_days,
                2
            )

    def total_payable(self):

        return round(
            self.amount + self.penalty,
            2
        )

    def __str__(self):

        return (
            f"EMI #{self.installment_number} | "
            f"Due: {self.due_date} | "
            f"Amount: ₹{self.amount} | "
            f"Status: {self.status.value}"
        )


# ============================================================
# LOAN
# ============================================================

class Loan:

    def __init__(
        self,
        loan_id,
        customer,
        product,
        requested_amount,
        tenure_months
    ):
        self.loan_id = loan_id
        self.customer = customer
        self.product = product

        self.requested_amount = requested_amount
        self.tenure_months = tenure_months

        self.approved_amount = 0
        self.interest_rate = product.annual_interest_rate
        self.emi = 0

        self.status = LoanStatus.APPLICATION

        self.application_date = date.today()
        self.approved_date = None

        self.repayments = []

    # --------------------------------------------------------
    # Approval
    # --------------------------------------------------------

    def approve(self, amount):

        if self.status != LoanStatus.APPLICATION:
            raise ValueError(
                "Loan is not in application state."
            )

        if amount > self.product.max_amount:
            raise ValueError(
                "Requested amount exceeds product limit."
            )

        self.approved_amount = amount

        self.status = LoanStatus.APPROVED

        self.approved_date = date.today()

        self.calculate_emi()

    # --------------------------------------------------------
    # EMI Calculation
    # --------------------------------------------------------

    def calculate_emi(self):

        principal = self.approved_amount

        monthly_rate = (
            self.interest_rate / 12 / 100
        )

        months = self.tenure_months

        if monthly_rate == 0:

            self.emi = round(
                principal / months,
                2
            )

        else:

            self.emi = round(
                principal
                * monthly_rate
                * (1 + monthly_rate) ** months
                /
                (
                    (1 + monthly_rate) ** months
                    - 1
                ),
                2
            )

    # --------------------------------------------------------
    # Activate Loan
    # --------------------------------------------------------

    def activate(self):

        if self.status != LoanStatus.APPROVED:
            raise ValueError(
                "Only approved loans can be activated."
            )

        self.status = LoanStatus.ACTIVE

        self.generate_repayment_schedule()

    # --------------------------------------------------------
    # Repayment Schedule
    # --------------------------------------------------------

    def generate_repayment_schedule(self):

        self.repayments.clear()

        principal_remaining = self.approved_amount

        monthly_rate = (
            self.interest_rate / 12 / 100
        )

        for month in range(
            1,
            self.tenure_months + 1
        ):

            interest = round(
                principal_remaining
                * monthly_rate,
                2
            )

            principal_component = round(
                self.emi - interest,
                2
            )

            # Correct rounding in final installment
            if month == self.tenure_months:

                principal_component = round(
                    principal_remaining,
                    2
                )

            repayment = Repayment(
                installment_number=month,
                due_date=(
                    self.application_date
                    + timedelta(days=30 * month)
                ),
                principal=principal_component,
                interest=interest
            )

            self.repayments.append(
                repayment
            )

            principal_remaining -= (
                principal_component
            )

            principal_remaining = max(
                principal_remaining,
                0
            )

    # --------------------------------------------------------
    # Payment
    # --------------------------------------------------------

    def make_payment(
        self,
        installment_number,
        payment_date
    ):

        repayment = self.get_repayment(
            installment_number
        )

        repayment.pay(payment_date)

        self.check_completion()

    # --------------------------------------------------------
    # Find Repayment
    # --------------------------------------------------------

    def get_repayment(
        self,
        installment_number
    ):

        for repayment in self.repayments:

            if (
                repayment.installment_number
                == installment_number
            ):
                return repayment

        raise ValueError(
            "Installment not found."
        )

    # --------------------------------------------------------
    # Overdue Detection
    # --------------------------------------------------------

    def check_overdue(self, today):

        if self.status != LoanStatus.ACTIVE:
            return

        for repayment in self.repayments:

            repayment.check_overdue(today)

        overdue_count = sum(
            1
            for repayment in self.repayments
            if repayment.status
            == PaymentStatus.OVERDUE
        )

        if overdue_count >= 3:

            self.status = LoanStatus.DEFAULTED

    # --------------------------------------------------------
    # Completion
    # --------------------------------------------------------

    def check_completion(self):

        if not self.repayments:
            return

        all_paid = all(
            repayment.status
            == PaymentStatus.PAID
            for repayment in self.repayments
        )

        if all_paid:

            self.status = LoanStatus.COMPLETED

    # --------------------------------------------------------
    # Outstanding Amount
    # --------------------------------------------------------

    def outstanding_amount(self):

        return round(
            sum(
                repayment.total_payable()
                for repayment in self.repayments
                if repayment.status
                != PaymentStatus.PAID
            ),
            2
        )

    # --------------------------------------------------------
    # Total Interest
    # --------------------------------------------------------

    def total_interest(self):

        return round(
            sum(
                repayment.interest
                for repayment in self.repayments
            ),
            2
        )

    # --------------------------------------------------------
    # Paid Installments
    # --------------------------------------------------------

    def paid_installments(self):

        return sum(
            1
            for repayment in self.repayments
            if repayment.status
            == PaymentStatus.PAID
        )

    # --------------------------------------------------------
    # Loan Summary
    # --------------------------------------------------------

    def summary(self):

        print(
            f"\nLoan: {self.loan_id}"
        )

        print(
            f"Customer: "
            f"{self.customer.name}"
        )

        print(
            f"Product: "
            f"{self.product.name}"
        )

        print(
            f"Principal: "
            f"₹{self.approved_amount}"
        )

        print(
            f"Interest Rate: "
            f"{self.interest_rate}%"
        )

        print(
            f"Tenure: "
            f"{self.tenure_months} months"
        )

        print(
            f"EMI: "
            f"₹{self.emi}"
        )

        print(
            f"Status: "
            f"{self.status.value}"
        )

        print(
            f"Paid Installments: "
            f"{self.paid_installments()}/"
            f"{self.tenure_months}"
        )

        print(
            f"Outstanding: "
            f"₹{self.outstanding_amount()}"
        )


# ============================================================
# CREDIT SCORING ENGINE
# ============================================================

class CreditScoringEngine:

    @staticmethod
    def calculate_score(customer):

        score = customer.credit_score

        # Existing debt affects eligibility
        debt_ratio = (
            customer.debt_to_income_ratio()
        )

        if debt_ratio > 0.5:
            score -= 50

        elif debt_ratio > 0.4:
            score -= 25

        # Employment stability
        if (
            customer.employment_type
            == EmploymentType.SALARIED
        ):
            score += 10

        elif (
            customer.employment_type
            == EmploymentType.BUSINESS
        ):
            score += 5

        return max(
            min(score, 900),
            300
        )


# ============================================================
# LOAN ELIGIBILITY ENGINE
# ============================================================

class LoanEligibilityEngine:

    @staticmethod
    def evaluate(customer, product, amount, tenure):

        score = CreditScoringEngine.calculate_score(
            customer
        )

        if score < product.min_credit_score:

            return False, (
                f"Credit score {score} is below "
                f"required {product.min_credit_score}"
            )

        if amount > product.max_amount:

            return False, (
                "Requested amount exceeds "
                "maximum loan amount."
            )

        if tenure > product.max_tenure_months:

            return False, (
                "Requested tenure exceeds "
                "product limit."
            )

        # Approximate EMI affordability
        monthly_rate = (
            product.annual_interest_rate
            / 12
            / 100
        )

        emi = (
            amount
            * monthly_rate
            * (1 + monthly_rate) ** tenure
            /
            (
                (1 + monthly_rate) ** tenure
                - 1
            )
        )

        existing_emi = (
            customer.total_monthly_emi()
        )

        total_emi = existing_emi + emi

        if total_emi > customer.monthly_income * 0.5:

            return False, (
                "EMI exceeds 50% of monthly income."
            )

        return True, (
            f"Eligible. Credit score: {score}"
        )


# ============================================================
# LOAN MANAGEMENT SYSTEM
# ============================================================

class LoanManagementSystem:

    def __init__(self):

        self.customers = {}
        self.products = {}
        self.loans = {}

    # --------------------------------------------------------
    # Registration
    # --------------------------------------------------------

    def add_customer(self, customer):

        self.customers[
            customer.customer_id
        ] = customer

    def add_product(self, product):

        self.products[
            product.product_id
        ] = product

    # --------------------------------------------------------
    # Loan Application
    # --------------------------------------------------------

    def apply_for_loan(
        self,
        loan_id,
        customer_id,
        product_id,
        amount,
        tenure
    ):

        customer = self.customers[
            customer_id
        ]

        product = self.products[
            product_id
        ]

        eligible, reason = (
            LoanEligibilityEngine.evaluate(
                customer,
                product,
                amount,
                tenure
            )
        )

        print(
            f"\nLoan Application: {loan_id}"
        )

        print(
            f"Customer: {customer.name}"
        )

        print(
            f"Decision: {reason}"
        )

        if not eligible:

            loan = Loan(
                loan_id,
                customer,
                product,
                amount,
                tenure
            )

            loan.status = LoanStatus.REJECTED

            self.loans[loan_id] = loan

            return loan

        loan = Loan(
            loan_id,
            customer,
            product,
            amount,
            tenure
        )

        loan.approve(amount)

        customer.add_loan(loan)

        self.loans[loan_id] = loan

        return loan

    # --------------------------------------------------------
    # Activate
    # --------------------------------------------------------

    def activate_loan(self, loan_id):

        loan = self.loans[loan_id]

        loan.activate()

    # --------------------------------------------------------
    # Process Payment
    # --------------------------------------------------------

    def process_payment(
        self,
        loan_id,
        installment_number,
        payment_date
    ):

        loan = self.loans[loan_id]

        loan.make_payment(
            installment_number,
            payment_date
        )

    # --------------------------------------------------------
    # Daily Loan Monitoring
    # --------------------------------------------------------

    def daily_monitoring(self, today):

        print(
            "\n========== DAILY LOAN MONITORING =========="
        )

        for loan in self.loans.values():

            loan.check_overdue(today)

            if loan.status == LoanStatus.DEFAULTED:

                print(
                    f"{loan.loan_id}: "
                    f"DEFAULTED"
                )

            else:

                print(
                    f"{loan.loan_id}: "
                    f"{loan.status.value}"
                )

    # --------------------------------------------------------
    # Portfolio Report
    # --------------------------------------------------------

    def portfolio_report(self):

        print(
            "\n========== LOAN PORTFOLIO =========="
        )

        total_disbursed = 0
        total_outstanding = 0

        for loan in self.loans.values():

            if loan.status in (
                LoanStatus.ACTIVE,
                LoanStatus.COMPLETED
            ):

                total_disbursed += (
                    loan.approved_amount
                )

                total_outstanding += (
                    loan.outstanding_amount()
                )

        print(
            f"Total Disbursed: "
            f"₹{total_disbursed}"
        )

        print(
            f"Total Outstanding: "
            f"₹{total_outstanding}"
        )

        print(
            f"Total Loans: "
            f"{len(self.loans)}"
        )


# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":

    system = LoanManagementSystem()

    # ========================================================
    # LOAN PRODUCTS
    # ========================================================

    personal_loan = LoanProduct(
        "LP001",
        "Personal Loan",
        min_credit_score=700,
        max_amount=1_000_000,
        annual_interest_rate=12.5,
        max_tenure_months=60
    )

    premium_loan = LoanProduct(
        "LP002",
        "Premium Personal Loan",
        min_credit_score=750,
        max_amount=2_500_000,
        annual_interest_rate=10.5,
        max_tenure_months=84
    )

    system.add_product(personal_loan)
    system.add_product(premium_loan)

    # ========================================================
    # CUSTOMERS
    # ========================================================

    customer1 = Customer(
        "C001",
        "Rishav",
        25,
        90_000,
        EmploymentType.SALARIED,
        760
    )

    customer2 = Customer(
        "C002",
        "Aman",
        31,
        45_000,
        EmploymentType.SALARIED,
        650
    )

    customer3 = Customer(
        "C003",
        "Rahul",
        40,
        150_000,
        EmploymentType.BUSINESS,
        810
    )

    system.add_customer(customer1)
    system.add_customer(customer2)
    system.add_customer(customer3)

    # ========================================================
    # LOAN 1
    # ========================================================

    loan1 = system.apply_for_loan(
        "L001",
        "C001",
        "LP001",
        amount=500_000,
        tenure=36
    )

    # ========================================================
    # LOAN 2
    # ========================================================

    loan2 = system.apply_for_loan(
        "L002",
        "C002",
        "LP001",
        amount=700_000,
        tenure=48
    )

    # ========================================================
    # LOAN 3
    # ========================================================

    loan3 = system.apply_for_loan(
        "L003",
        "C003",
        "LP002",
        amount=1_500_000,
        tenure=60
    )

    # ========================================================
    # ACTIVATE APPROVED LOANS
    # ========================================================

    if loan1.status == LoanStatus.APPROVED:

        system.activate_loan("L001")

    if loan3.status == LoanStatus.APPROVED:

        system.activate_loan("L003")

    # ========================================================
    # PRINT EMI
    # ========================================================

    print(
        "\n========== EMI DETAILS =========="
    )

    print(
        f"Loan L001 EMI: "
        f"₹{loan1.emi}"
    )

    print(
        f"Loan L003 EMI: "
        f"₹{loan3.emi}"
    )

    # ========================================================
    # MAKE SOME PAYMENTS
    # ========================================================

    system.process_payment(
        "L001",
        1,
        date(2026, 10, 1)
    )

    system.process_payment(
        "L001",
        2,
        date(2026, 11, 1)
    )

    system.process_payment(
        "L003",
        1,
        date(2026, 10, 1)
    )

    # ========================================================
    # CHECK LOAN
    # ========================================================

    loan1.summary()

    loan3.summary()

    # ========================================================
    # REPAYMENT SCHEDULE
    # ========================================================

    print(
        "\n========== L001 REPAYMENT SCHEDULE =========="
    )

    for repayment in loan1.repayments[:6]:

        print(repayment)

    # ========================================================
    # SIMULATE OVERDUE
    # ========================================================

    future_date = date(
        2027,
        1,
        20
    )

    system.daily_monitoring(
        future_date
    )

    # ========================================================
    # PORTFOLIO
    # ========================================================

    system.portfolio_report()