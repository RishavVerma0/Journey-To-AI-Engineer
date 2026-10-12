class RideBooking:
    def __init__(self):
        self.rides = {}
        self.next_ride_id = 1

    def book_ride(self, passenger, pickup, destination, distance):
        ride_id = self.next_ride_id
        fare = distance * 15

        self.rides[ride_id] = {
            "passenger": passenger,
            "pickup": pickup,
            "destination": destination,
            "distance": distance,
            "fare": fare,
            "status": "Booked"
        }

        self.next_ride_id += 1
        print(f"Ride #{ride_id} booked. Fare: ₹{fare}")
        return ride_id

    def complete_ride(self, ride_id):
        ride = self.rides.get(ride_id)

        if ride and ride["status"] == "Booked":
            ride["status"] = "Completed"
            print(f"Ride #{ride_id} completed.")
        else:
            print("Invalid ride or ride already completed.")

    def show_rides(self):
        for ride_id, ride in self.rides.items():
            print(
                f"Ride #{ride_id} | {ride['passenger']} | "
                f"{ride['pickup']} → {ride['destination']} | "
                f"₹{ride['fare']} | {ride['status']}"
            )


app = RideBooking()

ride1 = app.book_ride("Rahul", "Home", "Office", 12)
ride2 = app.book_ride("Priya", "Mall", "Airport", 25)

app.complete_ride(ride1)
app.complete_ride(ride1)

app.show_rides()