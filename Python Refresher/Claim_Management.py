from datetime import datetime
from enum import Enum


# =========================================================
# ENUMS
# =========================================================

class ClaimStatus(Enum):
    SUBMITTED = "Submitted"
    UNDER_REVIEW = "Under Review"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    SETTLED = "Settled"


class ClaimType(Enum):
    VEHICLE = "Vehicle"
    HEALTH = "Health"
    TRAVEL = "Travel"
    PROPERTY = "Property"


# =========================================================
# POLICY HOLDER
# =========================================================

class PolicyHolder:

    def __init__(self, customer_id, name, phone):

        self.customer_id = customer_id
        self.name = name
        self.phone = phone

        self.policies = []
        self.claims = []

    def add_policy(self, policy):

        self.policies.append(policy)

    def add_claim(self, claim):

        self.claims.append(claim)

    def get_active_policies(self):

        return [
            policy
            for policy in self.policies
            if policy.is_active()
        ]


# =========================================================
# INSURANCE POLICY
# =========================================================

class InsurancePolicy:

    def __init__(
        self,
        policy_number,
        policy_holder,
        claim_type,
        coverage_amount,
        start_date,
        end_date
    ):

        self.policy_number = policy_number
        self.policy_holder = policy_holder

        self.claim_type = claim_type

        self.coverage_amount = coverage_amount

        self.start_date = start_date
        self.end_date = end_date

    def is_active(self):

        today = datetime.now().date()

        return (
            self.start_date
            <= today
            <= self.end_date
        )

    def covers(self, claim_type):

        return self.claim_type == claim_type

    def display(self):

        print("\nPOLICY")

        print(
            "Policy Number:",
            self.policy_number
        )

        print(
            "Holder:",
            self.policy_holder.name
        )

        print(
            "Type:",
            self.claim_type.value
        )

        print(
            "Coverage:",
            f"₹{self.coverage_amount}"
        )

        print(
            "Active:",
            self.is_active()
        )


# =========================================================
# DOCUMENT
# =========================================================

class Document:

    def __init__(
        self,
        document_type,
        document_number
    ):

        self.document_type = document_type
        self.document_number = document_number

        self.verified = False

    def verify(self):

        if not self.document_number:

            raise ValueError(
                "Document number cannot be empty."
            )

        self.verified = True

    def __str__(self):

        status = (
            "Verified"
            if self.verified
            else "Not Verified"
        )

        return (
            f"{self.document_type} | "
            f"{self.document_number} | "
            f"{status}"
        )


# =========================================================
# CLAIM
# =========================================================

class Claim:

    counter = 1000

    def __init__(
        self,
        policy_holder,
        policy,
        claim_type,
        claimed_amount,
        description
    ):

        Claim.counter += 1

        self.claim_id = (
            f"CLM{Claim.counter}"
        )

        self.policy_holder = policy_holder
        self.policy = policy

        self.claim_type = claim_type

        self.claimed_amount = claimed_amount

        self.description = description

        self.status = ClaimStatus.SUBMITTED

        self.created_at = datetime.now()

        self.documents = []

        self.approved_amount = 0

        self.rejection_reason = None

        self.fraud_flags = []

        self.adjuster = None

    # -----------------------------------------------------
    # ADD DOCUMENT
    # -----------------------------------------------------

    def add_document(self, document):

        self.documents.append(document)

    # -----------------------------------------------------
    # CHECK DOCUMENTS
    # -----------------------------------------------------

    def all_documents_verified(self):

        if not self.documents:
            return False

        return all(
            document.verified
            for document in self.documents
        )

    # -----------------------------------------------------
    # ADD FRAUD FLAG
    # -----------------------------------------------------

    def add_fraud_flag(self, reason):

        self.fraud_flags.append(reason)

    # -----------------------------------------------------
    # MOVE TO REVIEW
    # -----------------------------------------------------

    def start_review(self):

        if self.status != ClaimStatus.SUBMITTED:

            raise Exception(
                "Only submitted claims "
                "can enter review."
            )

        self.status = ClaimStatus.UNDER_REVIEW

    # -----------------------------------------------------
    # APPROVE
    # -----------------------------------------------------

    def approve(self, amount):

        if self.status != ClaimStatus.UNDER_REVIEW:

            raise Exception(
                "Claim must be under review "
                "before approval."
            )

        if amount <= 0:

            raise ValueError(
                "Approved amount must be positive."
            )

        if amount > self.policy.coverage_amount:

            raise ValueError(
                "Approved amount exceeds "
                "policy coverage."
            )

        self.approved_amount = amount

        self.status = ClaimStatus.APPROVED

    # -----------------------------------------------------
    # REJECT
    # -----------------------------------------------------

    def reject(self, reason):

        if self.status not in (
            ClaimStatus.SUBMITTED,
            ClaimStatus.UNDER_REVIEW
        ):

            raise Exception(
                "Claim cannot be rejected "
                "in its current state."
            )

        self.rejection_reason = reason

        self.status = ClaimStatus.REJECTED

    # -----------------------------------------------------
    # SETTLE
    # -----------------------------------------------------

    def settle(self):

        if self.status != ClaimStatus.APPROVED:

            raise Exception(
                "Only approved claims "
                "can be settled."
            )

        self.status = ClaimStatus.SETTLED

    # -----------------------------------------------------
    # DISPLAY
    # -----------------------------------------------------

    def display(self):

        print("\n" + "=" * 65)

        print(
            "Claim ID:",
            self.claim_id
        )

        print(
            "Customer:",
            self.policy_holder.name
        )

        print(
            "Claim Type:",
            self.claim_type.value
        )

        print(
            "Claimed Amount:",
            f"₹{self.claimed_amount}"
        )

        print(
            "Approved Amount:",
            f"₹{self.approved_amount}"
        )

        print(
            "Status:",
            self.status.value
        )

        print(
            "Documents:",
            len(self.documents)
        )

        if self.fraud_flags:

            print(
                "Fraud Flags:",
                ", ".join(self.fraud_flags)
            )

        if self.rejection_reason:

            print(
                "Rejection Reason:",
                self.rejection_reason
            )

        print("=" * 65)


# =========================================================
# CLAIM ADJUSTER
# =========================================================

class ClaimAdjuster:

    def __init__(
        self,
        employee_id,
        name,
        specialization
    ):

        self.employee_id = employee_id
        self.name = name
        self.specialization = specialization

        self.assigned_claims = []

    # -----------------------------------------------------
    # ASSIGN CLAIM
    # -----------------------------------------------------

    def assign_claim(self, claim):

        if (
            claim.claim_type
            != self.specialization
        ):

            raise ValueError(
                "Adjuster does not specialize "
                "in this claim type."
            )

        claim.adjuster = self

        self.assigned_claims.append(claim)

    def __str__(self):

        return (
            f"{self.name} | "
            f"Specialization: "
            f"{self.specialization.value}"
        )


# =========================================================
# CLAIM RULE ENGINE
# =========================================================

class ClaimRuleEngine:

    @staticmethod
    def validate_claim(claim):

        errors = []

        # -----------------------------------------------
        # Policy validation
        # -----------------------------------------------

        if not claim.policy.is_active():

            errors.append(
                "Insurance policy is not active."
            )

        # -----------------------------------------------
        # Claim type validation
        # -----------------------------------------------

        if not claim.policy.covers(
            claim.claim_type
        ):

            errors.append(
                "Policy does not cover "
                "this claim type."
            )

        # -----------------------------------------------
        # Amount validation
        # -----------------------------------------------

        if (
            claim.claimed_amount
            > claim.policy.coverage_amount
        ):

            errors.append(
                "Claimed amount exceeds "
                "policy coverage."
            )

        # -----------------------------------------------
        # Document validation
        # -----------------------------------------------

        if not claim.all_documents_verified():

            errors.append(
                "Required documents "
                "are not verified."
            )

        return errors

    @staticmethod
    def calculate_approved_amount(claim):

        # Simple business rule:
        # insurer does not automatically
        # approve the entire claimed amount.

        amount = claim.claimed_amount

        # Large claims get a 10% deduction
        # for this example.

        if amount > 100000:

            amount *= 0.90

        # Never exceed policy coverage.

        amount = min(
            amount,
            claim.policy.coverage_amount
        )

        return amount

    @staticmethod
    def detect_fraud_risk(claim):

        # Rule 1
        if claim.claimed_amount > 500000:

            claim.add_fraud_flag(
                "Very high claim amount"
            )

        # Rule 2
        if len(claim.documents) < 2:

            claim.add_fraud_flag(
                "Insufficient documentation"
            )

        # Rule 3
        if (
            claim.claimed_amount
            > claim.policy.coverage_amount
        ):

            claim.add_fraud_flag(
                "Claim exceeds policy coverage"
            )

        return claim.fraud_flags


# =========================================================
# CLAIM MANAGEMENT SYSTEM
# =========================================================

class ClaimManagementSystem:

    def __init__(self):

        self.customers = {}
        self.policies = {}
        self.claims = {}
        self.adjusters = {}

    # -----------------------------------------------------
    # CUSTOMER
    # -----------------------------------------------------

    def register_customer(self, customer):

        self.customers[
            customer.customer_id
        ] = customer

    # -----------------------------------------------------
    # POLICY
    # -----------------------------------------------------

    def register_policy(self, policy):

        self.policies[
            policy.policy_number
        ] = policy

        policy.policy_holder.add_policy(
            policy
        )

    # -----------------------------------------------------
    # ADJUSTER
    # -----------------------------------------------------

    def register_adjuster(self, adjuster):

        self.adjusters[
            adjuster.employee_id
        ] = adjuster

    # -----------------------------------------------------
    # CREATE CLAIM
    # -----------------------------------------------------

    def create_claim(
        self,
        customer_id,
        policy_number,
        claim_type,
        amount,
        description
    ):

        if customer_id not in self.customers:

            raise ValueError(
                "Customer not found."
            )

        if policy_number not in self.policies:

            raise ValueError(
                "Policy not found."
            )

        customer = self.customers[
            customer_id
        ]

        policy = self.policies[
            policy_number
        ]

        claim = Claim(
            customer,
            policy,
            claim_type,
            amount,
            description
        )

        customer.add_claim(claim)

        self.claims[
            claim.claim_id
        ] = claim

        return claim

    # -----------------------------------------------------
    # AUTOMATIC PROCESSING
    # -----------------------------------------------------

    def process_claim(self, claim):

        print(
            f"\nProcessing {claim.claim_id}..."
        )

        # -----------------------------------------------
        # Detect potential fraud indicators
        # -----------------------------------------------

        ClaimRuleEngine.detect_fraud_risk(
            claim
        )

        # -----------------------------------------------
        # Validate claim
        # -----------------------------------------------

        errors = (
            ClaimRuleEngine.validate_claim(
                claim
            )
        )

        if errors:

            claim.reject(
                "; ".join(errors)
            )

            print(
                "Claim rejected."
            )

            return

        # -----------------------------------------------
        # Start review
        # -----------------------------------------------

        claim.start_review()

        # -----------------------------------------------
        # Calculate approved amount
        # -----------------------------------------------

        approved_amount = (
            ClaimRuleEngine
            .calculate_approved_amount(
                claim
            )
        )

        claim.approve(
            approved_amount
        )

        print(
            f"Claim approved for "
            f"₹{approved_amount:.2f}"
        )

    # -----------------------------------------------------
    # SEARCH
    # -----------------------------------------------------

    def search_claims_by_customer(
        self,
        customer_id
    ):

        return [
            claim

            for claim in self.claims.values()

            if (
                claim.policy_holder.customer_id
                == customer_id
            )
        ]


# =========================================================
# DEMO
# =========================================================

system = ClaimManagementSystem()


# =========================================================
# CUSTOMER
# =========================================================

customer = PolicyHolder(
    "C101",
    "Rishav",
    "9876543210"
)

system.register_customer(customer)


# =========================================================
# POLICY
# =========================================================

policy = InsurancePolicy(
    policy_number="POL1001",
    policy_holder=customer,
    claim_type=ClaimType.VEHICLE,
    coverage_amount=500000,
    start_date=datetime(2026, 1, 1).date(),
    end_date=datetime(2027, 1, 1).date()
)

system.register_policy(policy)

policy.display()


# =========================================================
# ADJUSTER
# =========================================================

adjuster = ClaimAdjuster(
    "A101",
    "Amit",
    ClaimType.VEHICLE
)

system.register_adjuster(adjuster)


# =========================================================
# CREATE CLAIM
# =========================================================

claim = system.create_claim(
    customer_id="C101",
    policy_number="POL1001",
    claim_type=ClaimType.VEHICLE,
    amount=180000,
    description=(
        "Vehicle damaged in road accident."
    )
)


# =========================================================
# ADD DOCUMENTS
# =========================================================

claim.add_document(
    Document(
        "FIR",
        "FIR12345"
    )
)

claim.add_document(
    Document(
        "Repair Estimate",
        "REP67890"
    )
)


# =========================================================
# VERIFY DOCUMENTS
# =========================================================

for document in claim.documents:

    document.verify()

    print(document)


# =========================================================
# ASSIGN ADJUSTER
# =========================================================

adjuster.assign_claim(claim)


# =========================================================
# PROCESS CLAIM
# =========================================================

system.process_claim(claim)


# =========================================================
# DISPLAY CLAIM
# =========================================================

claim.display()


# =========================================================
# SETTLEMENT
# =========================================================

if claim.status == ClaimStatus.APPROVED:

    claim.settle()

claim.display()


# =========================================================
# SECOND CLAIM
# =========================================================

claim2 = system.create_claim(
    customer_id="C101",
    policy_number="POL1001",
    claim_type=ClaimType.VEHICLE,
    amount=700000,
    description=(
        "Major vehicle damage."
    )
)

# Only one document
claim2.add_document(
    Document(
        "Repair Estimate",
        "REP99999"
    )
)

for document in claim2.documents:

    document.verify()


system.process_claim(claim2)

claim2.display()