from datetime import date, timedelta
from enum import Enum


# =========================================================
# ENUMS
# =========================================================

class RoomType(Enum):
    STANDARD = "Standard"
    DELUXE = "Deluxe"
    SUITE = "Suite"


class BookingStatus(Enum):
    CONFIRMED = "Confirmed"
    CANCELLED = "Cancelled"
    COMPLETED = "Completed"


# =========================================================
# GUEST
# =========================================================

class Guest:

    def __init__(self, guest_id, name, phone):

        self.guest_id = guest_id
        self.name = name
        self.phone = phone

        self.bookings = []

    def add_booking(self, booking):

        self.bookings.append(booking)

    def __str__(self):

        return f"{self.name} ({self.phone})"


# =========================================================
# ROOM
# =========================================================

class Room:

    def __init__(self, room_number, room_type, price):

        self.room_number = room_number
        self.room_type = room_type
        self.price = price

        self.bookings = []

    # -----------------------------------------------------
    # CHECK AVAILABILITY
    # -----------------------------------------------------

    def is_available(self, check_in, check_out):

        for booking in self.bookings:

            if booking.status == BookingStatus.CANCELLED:
                continue

            # Date overlap condition
            #
            # Existing:
            #       |----------|
            #
            # New:
            #             |----------|
            #
            # If they overlap -> room unavailable

            if (
                check_in < booking.check_out
                and check_out > booking.check_in
            ):
                return False

        return True

    # -----------------------------------------------------
    # ADD BOOKING
    # -----------------------------------------------------

    def add_booking(self, booking):

        if not self.is_available(
            booking.check_in,
            booking.check_out
        ):

            raise ValueError(
                f"Room {self.room_number} "
                f"is already booked."
            )

        self.bookings.append(booking)

    def __str__(self):

        return (
            f"Room {self.room_number} | "
            f"{self.room_type.value} | "
            f"₹{self.price}/night"
        )


# =========================================================
# PRICING ENGINE
# =========================================================

class PricingEngine:

    @staticmethod
    def calculate_base_price(room, nights):

        return room.price * nights

    @staticmethod
    def calculate_discount(
        base_price,
        nights
    ):

        # Long-stay discount

        if nights >= 7:
            return base_price * 0.15

        if nights >= 3:
            return base_price * 0.10

        return 0

    @staticmethod
    def calculate_tax(amount):

        return amount * 0.18

    @classmethod
    def calculate_total(cls, room, nights):

        base = cls.calculate_base_price(
            room,
            nights
        )

        discount = cls.calculate_discount(
            base,
            nights
        )

        taxable_amount = base - discount

        tax = cls.calculate_tax(
            taxable_amount
        )

        return {
            "base": base,
            "discount": discount,
            "tax": tax,
            "total": taxable_amount + tax
        }


# =========================================================
# BOOKING
# =========================================================

class Booking:

    counter = 1000

    def __init__(
        self,
        guest,
        room,
        check_in,
        check_out
    ):

        if check_out <= check_in:

            raise ValueError(
                "Check-out must be after check-in."
            )

        Booking.counter += 1

        self.booking_id = (
            f"BKG{Booking.counter}"
        )

        self.guest = guest
        self.room = room

        self.check_in = check_in
        self.check_out = check_out

        self.status = BookingStatus.CONFIRMED

        self.created_at = date.today()

        self.nights = (
            check_out - check_in
        ).days

        self.price_breakdown = (
            PricingEngine.calculate_total(
                room,
                self.nights
            )
        )

    # -----------------------------------------------------
    # CANCEL
    # -----------------------------------------------------

    def cancel(self):

        if self.status != BookingStatus.CONFIRMED:

            raise Exception(
                "Only confirmed bookings "
                "can be cancelled."
            )

        self.status = BookingStatus.CANCELLED

    # -----------------------------------------------------
    # COMPLETE
    # -----------------------------------------------------

    def complete(self):

        if self.status != BookingStatus.CONFIRMED:

            raise Exception(
                "Booking is not active."
            )

        self.status = BookingStatus.COMPLETED

    # -----------------------------------------------------
    # DISPLAY
    # -----------------------------------------------------

    def display(self):

        print("\n" + "=" * 60)

        print(
            f"Booking ID : {self.booking_id}"
        )

        print(
            f"Guest      : {self.guest.name}"
        )

        print(
            f"Room       : {self.room.room_number}"
        )

        print(
            f"Room Type  : "
            f"{self.room.room_type.value}"
        )

        print(
            f"Check-in   : {self.check_in}"
        )

        print(
            f"Check-out  : {self.check_out}"
        )

        print(
            f"Nights     : {self.nights}"
        )

        print(
            f"Status     : {self.status.value}"
        )

        print(
            f"Base Price : "
            f"₹{self.price_breakdown['base']:.2f}"
        )

        print(
            f"Discount   : "
            f"₹{self.price_breakdown['discount']:.2f}"
        )

        print(
            f"Tax        : "
            f"₹{self.price_breakdown['tax']:.2f}"
        )

        print(
            f"TOTAL      : "
            f"₹{self.price_breakdown['total']:.2f}"
        )

        print("=" * 60)


# =========================================================
# HOTEL
# =========================================================

class Hotel:

    def __init__(self, name):

        self.name = name

        self.rooms = {}
        self.guests = {}
        self.bookings = {}

    # -----------------------------------------------------
    # ADD ROOM
    # -----------------------------------------------------

    def add_room(self, room):

        if room.room_number in self.rooms:

            raise ValueError(
                "Room already exists."
            )

        self.rooms[
            room.room_number
        ] = room

    # -----------------------------------------------------
    # REGISTER GUEST
    # -----------------------------------------------------

    def register_guest(self, guest):

        self.guests[
            guest.guest_id
        ] = guest

    # -----------------------------------------------------
    # FIND AVAILABLE ROOM
    # -----------------------------------------------------

    def find_available_room(
        self,
        room_type,
        check_in,
        check_out
    ):

        for room in self.rooms.values():

            if (
                room.room_type == room_type
                and room.is_available(
                    check_in,
                    check_out
                )
            ):
                return room

        return None

    # -----------------------------------------------------
    # CREATE BOOKING
    # -----------------------------------------------------

    def create_booking(
        self,
        guest_id,
        room_type,
        check_in,
        check_out
    ):

        if guest_id not in self.guests:

            raise ValueError(
                "Guest not registered."
            )

        room = self.find_available_room(
            room_type,
            check_in,
            check_out
        )

        if room is None:

            raise ValueError(
                "No room available for "
                "the selected dates."
            )

        guest = self.guests[guest_id]

        booking = Booking(
            guest,
            room,
            check_in,
            check_out
        )

        room.add_booking(booking)

        guest.add_booking(booking)

        self.bookings[
            booking.booking_id
        ] = booking

        return booking

    # -----------------------------------------------------
    # SEARCH BOOKINGS
    # -----------------------------------------------------

    def search_bookings(self, guest_id):

        return [

            booking

            for booking in self.bookings.values()

            if booking.guest.guest_id == guest_id

        ]


# =========================================================
# DEMO
# =========================================================

hotel = Hotel("Grand Palace")


# Rooms

hotel.add_room(
    Room(
        101,
        RoomType.STANDARD,
        3000
    )
)

hotel.add_room(
    Room(
        102,
        RoomType.STANDARD,
        3000
    )
)

hotel.add_room(
    Room(
        201,
        RoomType.DELUXE,
        5000
    )
)

hotel.add_room(
    Room(
        301,
        RoomType.SUITE,
        9000
    )
)


# Guest

guest = Guest(
    "G101",
    "Rishav",
    "9876543210"
)

hotel.register_guest(guest)


# ---------------------------------------------------------
# FIRST BOOKING
# ---------------------------------------------------------

booking1 = hotel.create_booking(
    guest_id="G101",
    room_type=RoomType.DELUXE,
    check_in=date(2026, 10, 1),
    check_out=date(2026, 10, 6)
)

booking1.display()


# ---------------------------------------------------------
# SECOND BOOKING
# ---------------------------------------------------------

booking2 = hotel.create_booking(
    guest_id="G101",
    room_type=RoomType.STANDARD,
    check_in=date(2026, 10, 10),
    check_out=date(2026, 10, 20)
)

booking2.display()


# ---------------------------------------------------------
# CANCEL
# ---------------------------------------------------------

booking1.cancel()

print(
    "\nBooking cancelled:",
    booking1.booking_id
)


# Because booking1 is cancelled,
# the room becomes available again.

booking3 = hotel.create_booking(
    guest_id="G101",
    room_type=RoomType.DELUXE,
    check_in=date(2026, 10, 2),
    check_out=date(2026, 10, 4)
)

booking3.display()