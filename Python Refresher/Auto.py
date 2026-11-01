class SmartDevice:
    def __init__(self, name, device_type):
        self.name = name
        self.device_type = device_type
        self.is_on = False

    def toggle(self):
        self.is_on = not self.is_on
        status = "ON" if self.is_on else "OFF"
        print(f"{self.name} is now {status}")

    def show_status(self):
        print(f"{self.device_type} - {self.name}: "
              f"{'ON' if self.is_on else 'OFF'}")


light = SmartDevice("Living Room Light", "Light")
ac = SmartDevice("Bedroom AC", "Air Conditioner")

light.toggle()
ac.toggle()
light.toggle()

print("\nDevice Status:")
light.show_status()
ac.show_status()