class Car:
    total_cars = 0

    def __init__(self, brand, model, price_per_day):
        self.brand = brand
        self.model = model
        self.price_per_day = price_per_day
        self.available = True

        Car.total_cars += 1

    def rent(self, days):
        if not self.available:
            print(f"{self.model} is already rented")
            return

        self.available = False
        cost = self.price_per_day * days

        print(f"{self.model} rented for {days} days")
        print(f"Total cost: ₹{cost}")

    def return_car(self):
        if self.available:
            print(f"{self.model} was not rented")
            return

        self.available = True
        print(f"{self.model} returned successfully")

    @classmethod
    def fleet_size(cls):
        return cls.total_cars

    @staticmethod
    def is_valid_days(days):
        return isinstance(days, int) and days > 0


cars = [
    Car("Maruti", "Fronx", 1800),
    Car("Hyundai", "Creta", 2500),
    Car("Toyota", "Fortuner", 5000)
]

print("Fleet size:", Car.fleet_size())

days = 5

if Car.is_valid_days(days):
    cars[0].rent(days)

cars[0].rent(3)

cars[0].return_car()

cars[0].rent(2)