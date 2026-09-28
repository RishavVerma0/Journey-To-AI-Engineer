from enum import Enum
from datetime import date, timedelta


# ============================================================
# ENUMS
# ============================================================

class SubscriptionStatus(Enum):
    TRIAL = "Trial"
    ACTIVE = "Active"
    PAST_DUE = "Past Due"
    CANCELLED = "Cancelled"
    SUSPENDED = "Suspended"


class PaymentStatus(Enum):
    SUCCESS = "Success"
    FAILED = "Failed"
    PENDING = "Pending"


class InvoiceStatus(Enum):
    DRAFT = "Draft"
    ISSUED = "Issued"
    PAID = "Paid"
    OVERDUE = "Overdue"


# ============================================================
# PLAN
# ============================================================

class Plan:

    def __init__(
        self,
        plan_id,
        name,
        monthly_price,
        user_limit,
        api_limit,
        storage_limit_gb
    ):
        self.plan_id = plan_id
        self.name = name
        self.monthly_price = monthly_price
        self.user_limit = user_limit
        self.api_limit = api_limit
        self.storage_limit_gb = storage_limit_gb

    def can_add_users(self, current_users, new_users=1):
        return current_users + new_users <= self.user_limit

    def __str__(self):
        return (
            f"{self.name} | "
            f"₹{self.monthly_price}/month | "
            f"Users: {self.user_limit} | "
            f"API: {self.api_limit} | "
            f"Storage: {self.storage_limit_gb}GB"
        )


# ============================================================
# CUSTOMER
# ============================================================

class Customer:

    def __init__(self, customer_id, company_name, email):
        self.customer_id = customer_id
        self.company_name = company_name
        self.email = email

        self.users = []
        self.subscription = None
        self.invoices = []
        self.payments = []

    def add_user(self, user):

        if self.subscription is None:
            raise ValueError("Customer has no subscription.")

        if not self.subscription.plan.can_add_users(
            len(self.users)
        ):
            raise ValueError(
                f"User limit exceeded for "
                f"{self.subscription.plan.name} plan."
            )

        self.users.append(user)

    def add_invoice(self, invoice):
        self.invoices.append(invoice)

    def add_payment(self, payment):
        self.payments.append(payment)

    def outstanding_amount(self):

        return sum(
            invoice.amount
            for invoice in self.invoices
            if invoice.status != InvoiceStatus.PAID
        )


# ============================================================
# USER
# ============================================================

class User:

    def __init__(self, user_id, name, email, role):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.role = role

    def __str__(self):
        return f"{self.name} ({self.role})"


# ============================================================
# USAGE
# ============================================================

class Usage:

    def __init__(self):

        self.api_calls = 0
        self.storage_gb = 0

    def record_api_call(self, count=1):
        self.api_calls += count

    def add_storage(self, gb):
        self.storage_gb += gb

    def reset(self):
        self.api_calls = 0
        self.storage_gb = 0


# ============================================================
# SUBSCRIPTION
# ============================================================

class Subscription:

    def __init__(
        self,
        subscription_id,
        customer,
        plan,
        start_date,
        trial_days=0
    ):

        self.subscription_id = subscription_id
        self.customer = customer
        self.plan = plan

        self.start_date = start_date
        self.next_billing_date = start_date + timedelta(days=30)

        self.status = (
            SubscriptionStatus.TRIAL
            if trial_days > 0
            else SubscriptionStatus.ACTIVE
        )

        self.trial_end_date = (
            start_date + timedelta(days=trial_days)
            if trial_days > 0
            else None
        )

        self.usage = Usage()

    # --------------------------------------------------------
    # Trial
    # --------------------------------------------------------

    def activate_after_trial(self, today):

        if self.status != SubscriptionStatus.TRIAL:
            raise ValueError("Subscription is not in trial.")

        if today < self.trial_end_date:
            raise ValueError("Trial period has not ended.")

        self.status = SubscriptionStatus.ACTIVE

    # --------------------------------------------------------
    # Usage
    # --------------------------------------------------------

    def record_api_usage(self, count=1):

        if self.status not in (
            SubscriptionStatus.ACTIVE,
            SubscriptionStatus.TRIAL
        ):
            raise ValueError(
                "Subscription is not active."
            )

        if (
            self.usage.api_calls + count
            > self.plan.api_limit
        ):
            raise ValueError(
                f"API limit exceeded for "
                f"{self.plan.name} plan."
            )

        self.usage.record_api_call(count)

    def add_storage(self, gb):

        if (
            self.usage.storage_gb + gb
            > self.plan.storage_limit_gb
        ):
            raise ValueError(
                f"Storage limit exceeded for "
                f"{self.plan.name} plan."
            )

        self.usage.add_storage(gb)

    # --------------------------------------------------------
    # Upgrade
    # --------------------------------------------------------

    def upgrade(self, new_plan):

        if new_plan.monthly_price <= self.plan.monthly_price:
            raise ValueError(
                "Upgrade plan must cost more."
            )

        old_plan = self.plan
        self.plan = new_plan

        print(
            f"Subscription upgraded: "
            f"{old_plan.name} → {new_plan.name}"
        )

    # --------------------------------------------------------
    # Downgrade
    # --------------------------------------------------------

    def downgrade(self, new_plan):

        if new_plan.monthly_price >= self.plan.monthly_price:
            raise ValueError(
                "Downgrade plan must cost less."
            )

        if len(self.customer.users) > new_plan.user_limit:
            raise ValueError(
                "Cannot downgrade. "
                "Current users exceed new plan limit."
            )

        if self.usage.storage_gb > new_plan.storage_limit_gb:
            raise ValueError(
                "Cannot downgrade. "
                "Current storage exceeds new plan."
            )

        old_plan = self.plan
        self.plan = new_plan

        print(
            f"Subscription downgraded: "
            f"{old_plan.name} → {new_plan.name}"
        )

    # --------------------------------------------------------
    # Cancellation
    # --------------------------------------------------------

    def cancel(self):

        if self.status == SubscriptionStatus.CANCELLED:
            raise ValueError("Already cancelled.")

        self.status = SubscriptionStatus.CANCELLED

    # --------------------------------------------------------
    # Suspension
    # --------------------------------------------------------

    def suspend(self):

        self.status = SubscriptionStatus.SUSPENDED

    def resume(self):

        if self.status != SubscriptionStatus.SUSPENDED:
            raise ValueError(
                "Subscription is not suspended."
            )

        self.status = SubscriptionStatus.ACTIVE


# ============================================================
# INVOICE
# ============================================================

class Invoice:

    def __init__(
        self,
        invoice_id,
        customer,
        amount,
        issue_date,
        due_date
    ):

        self.invoice_id = invoice_id
        self.customer = customer

        self.amount = amount
        self.issue_date = issue_date
        self.due_date = due_date

        self.status = InvoiceStatus.DRAFT

    def issue(self):

        if self.status != InvoiceStatus.DRAFT:
            raise ValueError(
                "Only draft invoices can be issued."
            )

        self.status = InvoiceStatus.ISSUED

    def mark_paid(self):

        self.status = InvoiceStatus.PAID

    def check_overdue(self, today):

        if (
            self.status in (
                InvoiceStatus.ISSUED,
                InvoiceStatus.DRAFT
            )
            and today > self.due_date
        ):
            self.status = InvoiceStatus.OVERDUE

    def __str__(self):

        return (
            f"{self.invoice_id} | "
            f"₹{self.amount} | "
            f"{self.status.value}"
        )


# ============================================================
# PAYMENT
# ============================================================

class Payment:

    def __init__(
        self,
        payment_id,
        customer,
        invoice,
        amount
    ):

        self.payment_id = payment_id
        self.customer = customer
        self.invoice = invoice
        self.amount = amount

        self.status = PaymentStatus.PENDING

    def process(self, success=True):

        if success:

            self.status = PaymentStatus.SUCCESS
            self.invoice.mark_paid()

        else:

            self.status = PaymentStatus.FAILED


# ============================================================
# BILLING ENGINE
# ============================================================

class BillingEngine:

    TAX_RATE = 0.18

    @classmethod
    def calculate_invoice(cls, subscription):

        base_price = subscription.plan.monthly_price

        tax = base_price * cls.TAX_RATE

        total = base_price + tax

        return round(total, 2)

    @classmethod
    def calculate_proration(
        cls,
        old_plan,
        new_plan,
        remaining_days
    ):

        price_difference = (
            new_plan.monthly_price
            - old_plan.monthly_price
        )

        daily_difference = price_difference / 30

        return round(
            daily_difference * remaining_days,
            2
        )


# ============================================================
# BILLING SYSTEM
# ============================================================

class SaaSBillingSystem:

    def __init__(self):

        self.plans = {}
        self.customers = {}
        self.subscriptions = {}
        self.invoices = {}
        self.payments = {}

    # --------------------------------------------------------
    # Plan Management
    # --------------------------------------------------------

    def add_plan(self, plan):

        if plan.plan_id in self.plans:
            raise ValueError("Plan already exists.")

        self.plans[plan.plan_id] = plan

    # --------------------------------------------------------
    # Customer Management
    # --------------------------------------------------------

    def register_customer(self, customer):

        if customer.customer_id in self.customers:
            raise ValueError(
                "Customer already exists."
            )

        self.customers[customer.customer_id] = customer

    # --------------------------------------------------------
    # Subscription
    # --------------------------------------------------------

    def create_subscription(
        self,
        subscription_id,
        customer_id,
        plan_id,
        start_date,
        trial_days=0
    ):

        customer = self.customers[customer_id]
        plan = self.plans[plan_id]

        if customer.subscription is not None:
            raise ValueError(
                "Customer already has a subscription."
            )

        subscription = Subscription(
            subscription_id,
            customer,
            plan,
            start_date,
            trial_days
        )

        customer.subscription = subscription

        self.subscriptions[
            subscription_id
        ] = subscription

        return subscription

    # --------------------------------------------------------
    # Generate Invoice
    # --------------------------------------------------------

    def generate_invoice(
        self,
        customer_id,
        invoice_id,
        issue_date
    ):

        customer = self.customers[customer_id]

        if customer.subscription is None:
            raise ValueError(
                "Customer has no subscription."
            )

        amount = BillingEngine.calculate_invoice(
            customer.subscription
        )

        invoice = Invoice(
            invoice_id,
            customer,
            amount,
            issue_date,
            issue_date + timedelta(days=7)
        )

        invoice.issue()

        customer.add_invoice(invoice)

        self.invoices[invoice_id] = invoice

        return invoice

    # --------------------------------------------------------
    # Process Payment
    # --------------------------------------------------------

    def process_payment(
        self,
        payment_id,
        customer_id,
        invoice_id,
        success=True
    ):

        customer = self.customers[customer_id]
        invoice = self.invoices[invoice_id]

        payment = Payment(
            payment_id,
            customer,
            invoice,
            invoice.amount
        )

        payment.process(success)

        customer.add_payment(payment)

        self.payments[payment_id] = payment

        if payment.status == PaymentStatus.FAILED:

            customer.subscription.status = (
                SubscriptionStatus.PAST_DUE
            )

        return payment

    # --------------------------------------------------------
    # Upgrade
    # --------------------------------------------------------

    def upgrade_subscription(
        self,
        customer_id,
        new_plan_id,
        remaining_days
    ):

        customer = self.customers[customer_id]

        subscription = customer.subscription

        old_plan = subscription.plan
        new_plan = self.plans[new_plan_id]

        proration = BillingEngine.calculate_proration(
            old_plan,
            new_plan,
            remaining_days
        )

        subscription.upgrade(new_plan)

        print(
            f"Proration charge: ₹{proration}"
        )

        return proration

    # --------------------------------------------------------
    # Subscription Health Check
    # --------------------------------------------------------

    def run_billing_health_check(self, today):

        print("\n========== BILLING HEALTH CHECK ==========")

        for customer in self.customers.values():

            subscription = customer.subscription

            if subscription is None:
                continue

            for invoice in customer.invoices:

                invoice.check_overdue(today)

            overdue = [
                invoice
                for invoice in customer.invoices
                if invoice.status == InvoiceStatus.OVERDUE
            ]

            if overdue:

                subscription.status = (
                    SubscriptionStatus.PAST_DUE
                )

                print(
                    f"{customer.company_name}: "
                    f"PAST DUE"
                )

            else:

                print(
                    f"{customer.company_name}: "
                    f"{subscription.status.value}"
                )

    # --------------------------------------------------------
    # Customer Report
    # --------------------------------------------------------

    def customer_report(self, customer_id):

        customer = self.customers[customer_id]

        subscription = customer.subscription

        print("\n========== CUSTOMER REPORT ==========")

        print(f"Company: {customer.company_name}")
        print(f"Email: {customer.email}")

        if subscription:

            print(
                f"Plan: {subscription.plan.name}"
            )

            print(
                f"Subscription: "
                f"{subscription.status.value}"
            )

            print(
                f"API Usage: "
                f"{subscription.usage.api_calls}/"
                f"{subscription.plan.api_limit}"
            )

            print(
                f"Storage: "
                f"{subscription.usage.storage_gb}/"
                f"{subscription.plan.storage_limit_gb} GB"
            )

        print(f"Users: {len(customer.users)}")

        print("\nInvoices:")

        for invoice in customer.invoices:
            print(invoice)

        print(
            f"\nOutstanding: "
            f"₹{customer.outstanding_amount()}"
        )


# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":

    system = SaaSBillingSystem()

    # --------------------------------------------------------
    # Create Plans
    # --------------------------------------------------------

    starter = Plan(
        "P001",
        "Starter",
        999,
        user_limit=5,
        api_limit=10_000,
        storage_limit_gb=10
    )

    professional = Plan(
        "P002",
        "Professional",
        2_999,
        user_limit=20,
        api_limit=100_000,
        storage_limit_gb=100
    )

    enterprise = Plan(
        "P003",
        "Enterprise",
        9_999,
        user_limit=100,
        api_limit=1_000_000,
        storage_limit_gb=1_000
    )

    system.add_plan(starter)
    system.add_plan(professional)
    system.add_plan(enterprise)

    # --------------------------------------------------------
    # Customer
    # --------------------------------------------------------

    customer = Customer(
        "C001",
        "TechNova Solutions",
        "admin@technova.com"
    )

    system.register_customer(customer)

    # --------------------------------------------------------
    # Trial Subscription
    # --------------------------------------------------------

    subscription = system.create_subscription(
        "SUB001",
        "C001",
        "P001",
        date(2026, 9, 1),
        trial_days=14
    )

    print("\nSubscription created:")
    print(subscription.plan)

    # --------------------------------------------------------
    # Add Users
    # --------------------------------------------------------

    users = [
        User("U001", "Aman", "aman@technova.com", "Developer"),
        User("U002", "Priya", "priya@technova.com", "Developer"),
        User("U003", "Rahul", "rahul@technova.com", "Manager")
    ]

    for user in users:
        customer.add_user(user)

    # --------------------------------------------------------
    # Usage
    # --------------------------------------------------------

    subscription.record_api_usage(2500)
    subscription.add_storage(4)

    # --------------------------------------------------------
    # Activate Trial
    # --------------------------------------------------------

    subscription.activate_after_trial(
        date(2026, 9, 16)
    )

    print(
        "\nSubscription status:",
        subscription.status.value
    )

    # --------------------------------------------------------
    # Generate Invoice
    # --------------------------------------------------------

    invoice = system.generate_invoice(
        "C001",
        "INV001",
        date(2026, 9, 16)
    )

    print("\nGenerated invoice:")
    print(invoice)

    # --------------------------------------------------------
    # Process Payment
    # --------------------------------------------------------

    payment = system.process_payment(
        "PAY001",
        "C001",
        "INV001",
        success=True
    )

    print(
        "\nPayment status:",
        payment.status.value
    )

    # --------------------------------------------------------
    # Upgrade
    # --------------------------------------------------------

    print("\n========== UPGRADE ==========")

    system.upgrade_subscription(
        "C001",
        "P002",
        remaining_days=20
    )

    # --------------------------------------------------------
    # More Usage
    # --------------------------------------------------------

    subscription.record_api_usage(5000)
    subscription.add_storage(15)

    # --------------------------------------------------------
    # Customer Report
    # --------------------------------------------------------

    system.customer_report("C001")

    # --------------------------------------------------------
    # Billing Health Check
    # --------------------------------------------------------

    system.run_billing_health_check(
        date(2026, 9, 25)
    )