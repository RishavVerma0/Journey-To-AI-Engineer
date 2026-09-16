from datetime import datetime
from math import ceil


class Location:

    def __init__(self, city, latitude, longitude):
        self.city = city
        self.latitude = latitude
        self.longitude = longitude

    def distance_from(self, other):

        lat_difference = abs(
            self.latitude - other.latitude
        )

        lon_difference = abs(
            self.longitude - other.longitude
        )

        # Simplified distance calculation
        distance = (
            (lat_difference ** 2)
            + (lon_difference ** 2)
        ) ** 0.5

        return distance * 111

    def __str__(self):
        return self.city


class Driver:

    def __init__(
        self,
        driver_id,
        name,
        vehicle_number,
        vehicle_type
    ):
        self.driver_id = driver_id
        self.name = name
        self.vehicle_number = vehicle_number
        self.vehicle_type = vehicle_type

        self.is_available = True
        self.current_location = None
        self.total_rides = 0
        self.total_earnings = 0

    def assign_ride(self):

        if not self.is_available:
            raise ValueError(
                "Driver is already busy"
            )

        self.is_available = False

    def complete_ride(self, fare):

        self.is_available = True

        self.total_rides += 1

        self.total_earnings += fare

    def cancel_ride(self):

        self.is_available = True

    def show_details(self):

        print(
            f"{self.driver_id} | "
            f"{self.name} | "
            f"{self.vehicle_number} | "
            f"{self.vehicle_type} | "
            f"Available: {self.is_available}"
        )


class Rider:

    def __init__(self, rider_id, name, phone):
        self.rider_id = rider_id
        self.name = name
        self.phone = phone
        self.ride_history = []

    def add_ride(self, ride):
        self.ride_history.append(ride)

    def show_history(self):

        print(
            f"\n===== {self.name}'s RIDE HISTORY ====="
        )

        for ride in self.ride_history:

            print(
                f"Ride #{ride.ride_id} | "
                f"{ride.status} | "
                f"₹{ride.fare:.2f}"
            )


class FareCalculator:

    BASE_FARE = 50

    RATES = {
        "BIKE": 8,
        "AUTO": 12,
        "SEDAN": 18,
        "SUV": 25
    }

    @classmethod
    def calculate(cls, distance, vehicle_type):

        if vehicle_type not in cls.RATES:
            raise ValueError(
                "Unsupported vehicle type"
            )

        rate = cls.RATES[vehicle_type]

        fare = (
            cls.BASE_FARE
            + distance * rate
        )

        # Minimum fare
        return max(
            100,
            ceil(fare)
        )


class Ride:

    ride_counter = 5000

    def __init__(
        self,
        rider,
        pickup,
        destination,
        vehicle_type
    ):

        Ride.ride_counter += 1

        self.ride_id = Ride.ride_counter

        self.rider = rider
        self.pickup = pickup
        self.destination = destination
        self.vehicle_type = vehicle_type

        self.driver = None
        self.status = "REQUESTED"

        self.distance = pickup.distance_from(
            destination
        )

        self.fare = 0

        self.created_at = datetime.now()

    def assign_driver(self, driver):

        if self.status != "REQUESTED":
            raise ValueError(
                "Ride cannot be assigned"
            )

        if driver.vehicle_type != self.vehicle_type:
            raise ValueError(
                "Vehicle type mismatch"
            )

        driver.assign_ride()

        self.driver = driver

        self.fare = FareCalculator.calculate(
            self.distance,
            self.vehicle_type
        )

        self.status = "DRIVER_ASSIGNED"

    def start(self):

        if self.driver is None:
            raise ValueError(
                "No driver assigned"
            )

        if self.status != "DRIVER_ASSIGNED":
            raise ValueError(
                "Ride cannot be started"
            )

        self.status = "ONGOING"

    def complete(self):

        if self.status != "ONGOING":
            raise ValueError(
                "Ride is not ongoing"
            )

        assert self.driver is not None
        self.driver.complete_ride(
            self.fare
        )

        self.status = "COMPLETED"

    def cancel(self):

        if self.status == "COMPLETED":
            raise ValueError(
                "Completed ride cannot be cancelled"
            )

        if self.driver:
            self.driver.cancel_ride()

        self.status = "CANCELLED"

    def show_details(self):

        print("\n========== RIDE ==========")

        print(f"Ride ID     : {self.ride_id}")
        print(f"Rider       : {self.rider.name}")
        print(f"Pickup      : {self.pickup}")
        print(f"Destination : {self.destination}")
        print(f"Vehicle     : {self.vehicle_type}")
        print(f"Distance    : {self.distance:.2f} km")

        if self.driver:
            print(
                f"Driver      : {self.driver.name}"
            )

        print(f"Fare        : ₹{self.fare:.2f}")
        print(f"Status      : {self.status}")


class CabService:

    def __init__(self, name):
        self.name = name
        self.drivers = {}
        self.riders = {}
        self.rides = {}

    def register_driver(self, driver):

        if driver.driver_id in self.drivers:
            raise ValueError(
                "Driver already registered"
            )

        self.drivers[
            driver.driver_id
        ] = driver

    def register_rider(self, rider):

        if rider.rider_id in self.riders:
            raise ValueError(
                "Rider already registered"
            )

        self.riders[
            rider.rider_id
        ] = rider

    def find_available_driver(
        self,
        vehicle_type
    ):

        for driver in self.drivers.values():

            if (
                driver.vehicle_type == vehicle_type
                and driver.is_available
            ):
                return driver

        return None

    def request_ride(
        self,
        rider,
        pickup,
        destination,
        vehicle_type
    ):

        driver = self.find_available_driver(
            vehicle_type
        )

        if driver is None:
            raise ValueError(
                "No driver available"
            )

        ride = Ride(
            rider,
            pickup,
            destination,
            vehicle_type
        )

        ride.assign_driver(driver)

        self.rides[
            ride.ride_id
        ] = ride

        rider.add_ride(ride)

        return ride


class Payment:

    def pay(self, ride, amount):

        if ride.status != "COMPLETED":
            raise ValueError(
                "Payment allowed only after ride completion"
            )

        if amount != ride.fare:
            raise ValueError(
                f"Incorrect amount. "
                f"Expected ₹{ride.fare:.2f}"
            )

        print(
            f"\nPayment successful: "
            f"₹{amount:.2f}"
        )


# =====================================================
# REAL-LIFE USAGE
# =====================================================

service = CabService(
    "Python Cabs"
)


driver1 = Driver(
    101,
    "Amit",
    "DL01AB1234",
    "SEDAN"
)

driver2 = Driver(
    102,
    "Rahul",
    "DL02CD5678",
    "SUV"
)


service.register_driver(driver1)
service.register_driver(driver2)


rider = Rider(
    501,
    "Rishav",
    "9876543210"
)

service.register_rider(rider)


pickup = Location(
    "Gurugram",
    28.4595,
    77.0266
)

destination = Location(
    "Delhi",
    28.6139,
    77.2090
)


ride = service.request_ride(
    rider,
    pickup,
    destination,
    "SEDAN"
)


ride.show_details()


ride.start()

print("\nRide started...")


ride.complete()

print("\nRide completed!")


ride.show_details()


payment = Payment()

payment.pay(
    ride,
    ride.fare
)


rider.show_history()


print("\n===== DRIVER DETAILS =====")

driver1.show_details()
driver2.show_details()