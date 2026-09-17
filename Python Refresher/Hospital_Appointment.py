from datetime import datetime


class Patient:
    def __init__(self, patient_id, name, age, phone):
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.phone = phone
        self.appointments = []
        self.medical_records = []

    def add_appointment(self, appointment):
        self.appointments.append(appointment)

    def add_record(self, record):
        self.medical_records.append(record)

    def show_history(self):
        print(f"\n===== {self.name}'S HISTORY =====")

        for appointment in self.appointments:
            print(
                f"Appointment #{appointment.appointment_id} | "
                f"{appointment.doctor.name} | "
                f"{appointment.status}"
            )

        print("\nMedical Records:")

        for record in self.medical_records:
            print(
                f"{record.date} | "
                f"Diagnosis: {record.diagnosis}"
            )


class Doctor:
    def __init__(
        self,
        doctor_id,
        name,
        specialization,
        consultation_fee
    ):
        self.doctor_id = doctor_id
        self.name = name
        self.specialization = specialization
        self.consultation_fee = consultation_fee
        self.available_slots = set()

    def add_slot(self, slot):
        self.available_slots.add(slot)

    def book_slot(self, slot):

        if slot not in self.available_slots:
            raise ValueError(
                "Doctor is not available at this time"
            )

        self.available_slots.remove(slot)

    def release_slot(self, slot):
        self.available_slots.add(slot)


class MedicalRecord:
    def __init__(
        self,
        patient,
        doctor,
        diagnosis,
        prescription
    ):
        self.patient = patient
        self.doctor = doctor
        self.diagnosis = diagnosis
        self.prescription = prescription
        self.date = datetime.now().strftime(
            "%Y-%m-%d"
        )


class Appointment:

    counter = 1000

    def __init__(
        self,
        patient,
        doctor,
        slot
    ):
        Appointment.counter += 1

        self.appointment_id = Appointment.counter
        self.patient = patient
        self.doctor = doctor
        self.slot = slot
        self.status = "BOOKED"

    def confirm(self):
        if self.status != "BOOKED":
            raise ValueError(
                "Appointment cannot be confirmed"
            )

        self.status = "CONFIRMED"

    def cancel(self):

        if self.status == "COMPLETED":
            raise ValueError(
                "Completed appointment cannot be cancelled"
            )

        self.doctor.release_slot(self.slot)
        self.status = "CANCELLED"

    def complete(
        self,
        diagnosis,
        prescription
    ):

        if self.status != "CONFIRMED":
            raise ValueError(
                "Appointment must be confirmed first"
            )

        record = MedicalRecord(
            self.patient,
            self.doctor,
            diagnosis,
            prescription
        )

        self.patient.add_record(record)

        self.status = "COMPLETED"


class Bill:

    def __init__(self, appointment):
        self.appointment = appointment
        self.items = []

    def add_item(self, name, price):
        self.items.append({
            "name": name,
            "price": price
        })

    @property
    def consultation_fee(self):
        return self.appointment.doctor.consultation_fee

    @property
    def subtotal(self):

        return (
            self.consultation_fee
            + sum(
                item["price"]
                for item in self.items
            )
        )

    @property
    def tax(self):
        return self.subtotal * 0.05

    @property
    def total(self):
        return self.subtotal + self.tax

    def print_bill(self):

        print("\n========== HOSPITAL BILL ==========")

        print(
            f"Patient: "
            f"{self.appointment.patient.name}"
        )

        print(
            f"Doctor: "
            f"{self.appointment.doctor.name}"
        )

        print(
            f"Consultation: "
            f"₹{self.consultation_fee:.2f}"
        )

        for item in self.items:
            print(
                f"{item['name']}: "
                f"₹{item['price']:.2f}"
            )

        print(
            f"Subtotal: ₹{self.subtotal:.2f}"
        )

        print(
            f"Tax: ₹{self.tax:.2f}"
        )

        print(
            f"TOTAL: ₹{self.total:.2f}"
        )


class Hospital:

    def __init__(self, name):
        self.name = name
        self.patients = {}
        self.doctors = {}
        self.appointments = {}

    def register_patient(self, patient):

        self.patients[
            patient.patient_id
        ] = patient

    def register_doctor(self, doctor):

        self.doctors[
            doctor.doctor_id
        ] = doctor

    def book_appointment(
        self,
        patient_id,
        doctor_id,
        slot
    ):

        patient = self.patients.get(patient_id)
        doctor = self.doctors.get(doctor_id)

        if patient is None:
            raise ValueError(
                "Patient not found"
            )

        if doctor is None:
            raise ValueError(
                "Doctor not found"
            )

        doctor.book_slot(slot)

        appointment = Appointment(
            patient,
            doctor,
            slot
        )

        patient.add_appointment(
            appointment
        )

        self.appointments[
            appointment.appointment_id
        ] = appointment

        return appointment


# ======================================
# REAL-LIFE USAGE
# ======================================

hospital = Hospital(
    "City Care Hospital"
)


doctor = Doctor(
    101,
    "Dr. Sharma",
    "Cardiology",
    800
)

doctor.add_slot("10:00 AM")
doctor.add_slot("11:00 AM")
doctor.add_slot("2:00 PM")


patient = Patient(
    501,
    "Rishav",
    25,
    "9876543210"
)


hospital.register_doctor(doctor)
hospital.register_patient(patient)


appointment = hospital.book_appointment(
    501,
    101,
    "10:00 AM"
)

print(
    f"Appointment #{appointment.appointment_id} "
    f"created"
)


appointment.confirm()

print("Appointment confirmed")


appointment.complete(
    diagnosis="Hypertension",
    prescription="Medication + follow-up"
)


bill = Bill(appointment)

bill.add_item(
    "Blood Test",
    500
)

bill.add_item(
    "ECG",
    700
)

bill.print_bill()


patient.show_history()