from datetime import datetime

class Vehicle:
    def __init__(self, number, vehicle_type):
        self.number = number
        self.vehicle_type = vehicle_type
        self.entry_time = datetime.now()


class ParkingLot:
    def __init__(self, capacity):
        self.capacity = capacity
        self.parked_vehicles = {}

    def park_vehicle(self, vehicle):
        if len(self.parked_vehicles) >= self.capacity:
            print("Parking Full!")
            return

        if vehicle.number in self.parked_vehicles:
            print("Vehicle is already parked!")
            return

        self.parked_vehicles[vehicle.number] = vehicle
        print(f"{vehicle.number} parked successfully.")

    def remove_vehicle(self, number):
        vehicle = self.parked_vehicles.pop(number, None)

        if vehicle is None:
            print("Vehicle not found!")
            return

        duration = (datetime.now() - vehicle.entry_time).total_seconds() / 3600
        fee = max(50, round(duration * 40))

        print(f"Vehicle: {number}")
        print(f"Parking Duration: {duration:.2f} hours")
        print(f"Parking Fee: ₹{fee}")


# Usage
lot = ParkingLot(2)

car1 = Vehicle("JH09AB1234", "Car")
car2 = Vehicle("JH09CD5678", "Bike")

lot.park_vehicle(car1)
lot.park_vehicle(car2)

lot.remove_vehicle("JH09AB1234")