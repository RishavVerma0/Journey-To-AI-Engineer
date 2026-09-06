class Ride:
    def __init__(self, customer, distance):
        self.customer = customer
        self.distance = distance

    def calculate_fare(self):
        raise NotImplementedError

    def display(self):
        print(f"Customer: {self.customer}")
        print(f"Distance: {self.distance} km")
        print(f"Fare: ₹{self.calculate_fare():.2f}")


class EconomyRide(Ride):
    def calculate_fare(self):
        base_fare = 50
        per_km = 12

        return base_fare + self.distance * per_km


class PremiumRide(Ride):
    def calculate_fare(self):
        base_fare = 100
        per_km = 20

        return base_fare + self.distance * per_km


class BikeRide(Ride):
    def calculate_fare(self):
        base_fare = 30
        per_km = 8

        return base_fare + self.distance * per_km


rides = [
    EconomyRide("Rishav", 10),
    PremiumRide("Aman", 10),
    BikeRide("Rahul", 10)
]

for ride in rides:
    ride.display()
    print("-" * 30)