class Vehicle:

    def __init__(self, vehicle_number, owner):
        self.vehicle_number = vehicle_number
        self.owner = owner

    def calculate_fee(self, hours):
        return hours * 20


class Car(Vehicle):

    def calculate_fee(self, hours):
        return hours * 50


class Bike(Vehicle):

    def calculate_fee(self, hours):
        return hours * 20


class ParkingLot:

    def __init__(self, capacity):
        self.__capacity = capacity
        self.__parked_vehicles = {}

    def park_vehicle(self, vehicle):
        if len(self.__parked_vehicles) < self.__capacity:
            self.__parked_vehicles[vehicle.vehicle_number] = vehicle
            print(f"{vehicle.vehicle_number} parked successfully.")
        else:
            print("Parking lot is full!")

    def remove_vehicle(self, vehicle_number, hours):
        vehicle = self.__parked_vehicles.pop(vehicle_number, None)

        if vehicle:
            fee = vehicle.calculate_fee(hours)
            print(f"Vehicle: {vehicle_number}")
            print(f"Owner: {vehicle.owner}")
            print(f"Parking Duration: {hours} hours")
            print(f"Total Parking Fee: ₹{fee}")
        else:
            print("Vehicle not found!")

    def available_slots(self):
        print(f"Available Slots: {self.__capacity - len(self.__parked_vehicles)}")


# Creating vehicles
car = Car("HR26AB1234", "Rishav")
bike = Bike("HR26XY5678", "Rahul")

# Creating parking lot
parking = ParkingLot(3)

# Parking operations
parking.park_vehicle(car)
parking.park_vehicle(bike)

parking.available_slots()

print("\n--- Vehicle Exit ---")
parking.remove_vehicle("HR26AB1234", 4)

parking.available_slots()