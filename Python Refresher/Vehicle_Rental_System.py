# 🚗 Vehicle Rental System — Inheritance + Polymorphism

class Vehicle:
    def __init__(self, vehicle_number, brand, rent_per_day):
        self.vehicle_number = vehicle_number
        self.brand = brand
        self.rent_per_day = rent_per_day

    def calculate_rent(self, days):
        return self.rent_per_day * days

    def display(self):
        print(f"Vehicle: {self.brand}")
        print(f"Number: {self.vehicle_number}")


class Car(Vehicle):
    def calculate_rent(self, days):
        base_rent = super().calculate_rent(days)

        if days >= 7:
            return base_rent * 0.90

        return base_rent


class Bike(Vehicle):
    def calculate_rent(self, days):
        base_rent = super().calculate_rent(days)

        if days >= 5:
            return base_rent * 0.95

        return base_rent


class Truck(Vehicle):
    def calculate_rent(self, days):
        base_rent = super().calculate_rent(days)

        insurance = 500

        return base_rent + insurance


vehicles = [
    Car("HR26AB1234", "Maruti", 1500),
    Bike("BR10XY5678", "Honda", 600),
    Truck("DL01TR9999", "Tata", 3000)
]

days = 7

for vehicle in vehicles:
    vehicle.display()
    print(f"Rent for {days} days: ₹{vehicle.calculate_rent(days)}")
    print("-" * 30)