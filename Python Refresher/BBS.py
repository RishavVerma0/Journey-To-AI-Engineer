class Bus:
    def __init__(self, total_seats):
        self.total_seats = total_seats
        self.booked_seats = []

    def book_seat(self, seat_number):
        if seat_number in self.booked_seats:
            print("Seat already booked")
        elif seat_number > self.total_seats or seat_number < 1:
            print("Invalid seat number")
        else:
            self.booked_seats.append(seat_number)
            print(f"Seat {seat_number} booked")

    def available_seats(self):
        return self.total_seats - len(self.booked_seats)

    def show_status(self):
        print("Booked:", self.booked_seats)
        print("Available seats:", self.available_seats())


bus = Bus(20)

bus.book_seat(5)
bus.book_seat(10)
bus.book_seat(5)
bus.book_seat(21)

bus.show_status()