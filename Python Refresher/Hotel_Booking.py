class Room:
    def __init__(self, room_number, price):
        self.room_number = room_number
        self.price = price
        self.__booked = False

    def book(self):
        if self.__booked:
            return False

        self.__booked = True
        return True

    def checkout(self):
        self.__booked = False

    def is_available(self):
        return not self.__booked

    def calculate_bill(self, days):
        return self.price * days


class DeluxeRoom(Room):
    def calculate_bill(self, days):
        base_price = super().calculate_bill(days)
        service_charge = 500 * days

        return base_price + service_charge


class SuiteRoom(Room):
    def calculate_bill(self, days):
        base_price = super().calculate_bill(days)

        if days >= 5:
            return base_price * 0.90

        return base_price


class Hotel:
    def __init__(self):
        self.rooms = []

    def add_room(self, room):
        self.rooms.append(room)

    def book_room(self, room_number, days):
        for room in self.rooms:
            if room.room_number == room_number:

                if room.book():
                    bill = room.calculate_bill(days)
                    print(f"Room {room_number} booked")
                    print(f"Total bill: ₹{bill}")
                else:
                    print(f"Room {room_number} is already booked")

                return

        print("Room not found")

    def checkout(self, room_number):
        for room in self.rooms:
            if room.room_number == room_number:
                room.checkout()
                print(f"Room {room_number} checked out")
                return

        print("Room not found")


hotel = Hotel()

hotel.add_room(Room(101, 2000))
hotel.add_room(DeluxeRoom(201, 3500))
hotel.add_room(SuiteRoom(301, 6000))

hotel.book_room(201, 3)

print()

hotel.book_room(201, 2)

print()

hotel.checkout(201)

print()

hotel.book_room(301, 5)