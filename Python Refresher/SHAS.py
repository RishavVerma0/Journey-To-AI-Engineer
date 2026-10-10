class Hospital:
    def __init__(self):
        self.appointments = []

    def book_appointment(self, patient, doctor, time):
        for appointment in self.appointments:
            if appointment["doctor"] == doctor and appointment["time"] == time:
                print("Doctor is already booked at this time.")
                return

        self.appointments.append({
            "patient": patient,
            "doctor": doctor,
            "time": time
        })
        print(f"Appointment booked for {patient}.")

    def cancel_appointment(self, patient):
        for appointment in self.appointments:
            if appointment["patient"] == patient:
                self.appointments.remove(appointment)
                print(f"Appointment cancelled for {patient}.")
                return

        print("Appointment not found.")

    def show_appointments(self):
        for appointment in self.appointments:
            print(
                f"{appointment['patient']} | "
                f"Dr. {appointment['doctor']} | "
                f"{appointment['time']}"
            )


hospital = Hospital()

hospital.book_appointment("Rahul", "Sharma", "10:00 AM")
hospital.book_appointment("Priya", "Sharma", "10:00 AM")
hospital.book_appointment("Amit", "Verma", "10:00 AM")

hospital.cancel_appointment("Rahul")

hospital.show_appointments()