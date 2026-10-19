class WeatherMonitor:
    def __init__(self, city):
        self.city = city
        self.readings = []

    def add_reading(self, temperature, humidity):
        if not 0 <= humidity <= 100:
            print("Invalid humidity")
            return

        self.readings.append({
            "temperature": temperature,
            "humidity": humidity
        })

    def average_temperature(self):
        if not self.readings:
            return 0

        return sum(
            reading["temperature"] for reading in self.readings
        ) / len(self.readings)

    def hottest_reading(self):
        if not self.readings:
            return None

        return max(
            self.readings,
            key=lambda reading: reading["temperature"]
        )

    def show_report(self):
        print(f"City: {self.city}")
        print(f"Readings Recorded: {len(self.readings)}")
        print(f"Average Temperature: {self.average_temperature():.1f}°C")

        hottest = self.hottest_reading()

        if hottest:
            print(f"Hottest Temperature: {hottest['temperature']}°C")
            print(f"Humidity: {hottest['humidity']}%")


weather = WeatherMonitor("Delhi")

weather.add_reading(32, 65)
weather.add_reading(36, 55)
weather.add_reading(30, 70)
weather.add_reading(39, 45)

weather.show_report()