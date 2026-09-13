class Doctor:
    def __init__(self, name, specialization):
        self.name = name
        self.specialization = specialization
        self.__appointments = []

    def book_appointment(self, patient):
        if patient in self.__appointments:
            print(f"{patient} already has an appointment")
            return False

        self.__appointments.append(patient)
        return True

    def cancel_appointment(self, patient):
        if patient not in self.__appointments:
            return False

        self.__appointments.remove(patient)
        return True

    def available_slots(self):
        return 10 - len(self.__appointments)

    def display(self):
        print(
            f"Dr. {self.name} | "
            f"{self.specialization} | "
            f"Available slots: {self.available_slots()}"
        )


class Hospital:
    def __init__(self):
        self.doctors = []

    def add_doctor(self, doctor):
        self.doctors.append(doctor)

    def find_doctor(self, specialization):
        return [
            doctor
            for doctor in self.doctors
            if doctor.specialization.lower() == specialization.lower()
        ]

    def book(self, doctor, patient):
        if doctor.book_appointment(patient):
            print(f"Appointment booked for {patient}")
        else:
            print("Unable to book appointment")


hospital = Hospital()

doctor1 = Doctor("Sharma", "Cardiologist")
doctor2 = Doctor("Verma", "Dermatologist")

hospital.add_doctor(doctor1)
hospital.add_doctor(doctor2)

hospital.book(doctor1, "Rishav")
hospital.book(doctor1, "Aman")
hospital.book(doctor2, "Rahul")

print()
doctor1.display()
doctor2.display()

print("\nCardiologists:")
for doctor in hospital.find_doctor("cardiologist"):
    print(doctor.name)