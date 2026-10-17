class Hotel:
    def __init__(self, total_rooms):
        self.rooms = {
            room_number: None
            for room_number in range(101, 101 + total_rooms)
        }

    def book_room(self, guest_name, room_number):
        if room_number not in self.rooms:
            print("Invalid room number")
            return

        if self.rooms[room_number] is not None:
            print("Room already occupied")
            return

        self.rooms[room_number] = guest_name
        print(f"Room {room_number} booked for {guest_name}")

    def checkout(self, room_number):
        if room_number not in self.rooms:
            print("Invalid room number")
        elif self.rooms[room_number] is None:
            print("Room is already available")
        else:
            print(f"{self.rooms[room_number]} checked out")
            self.rooms[room_number] = None

    def show_available_rooms(self):
        available = [
            room for room, guest in self.rooms.items()
            if guest is None
        ]

        print("Available rooms:", available)

    def show_occupancy(self):
        occupied = sum(
            guest is not None for guest in self.rooms.values()
        )

        print(f"Total Rooms: {len(self.rooms)}")
        print(f"Occupied: {occupied}")
        print(f"Available: {len(self.rooms) - occupied}")


hotel = Hotel(5)

hotel.book_room("Rahul", 101)
hotel.book_room("Priya", 102)
hotel.book_room("Amit", 101)

hotel.show_available_rooms()
hotel.checkout(101)

hotel.show_occupancy()