class WeatherAnalyzer:

    def __init__(self, weather_data):
        self.weather_data = weather_data

    def average_temperature(self):
        valid_temperatures = []

        for city, data in self.weather_data.items():
            temperature = data.get("temperature")

            if isinstance(temperature, (int, float)):
                valid_temperatures.append(temperature)

        if not valid_temperatures:
            return 0

        return sum(valid_temperatures) / len(valid_temperatures)

    def hottest_city(self):
        valid_data = {
            city: data
            for city, data in self.weather_data.items()
            if isinstance(data.get("temperature"), (int, float))
        }

        if not valid_data:
            return None

        return max(
            valid_data.items(),
            key=lambda item: item[1]["temperature"]
        )

    def coldest_city(self):
        valid_data = {
            city: data
            for city, data in self.weather_data.items()
            if isinstance(data.get("temperature"), (int, float))
        }

        if not valid_data:
            return None

        return min(
            valid_data.items(),
            key=lambda item: item[1]["temperature"]
        )

    def cities_above_temperature(self, threshold):
        return [
            city
            for city, data in self.weather_data.items()
            if isinstance(data.get("temperature"), (int, float))
            and data["temperature"] > threshold
        ]

    def sort_by_temperature(self, reverse=False):
        valid_data = [
            (city, data)
            for city, data in self.weather_data.items()
            if isinstance(data.get("temperature"), (int, float))
        ]

        return sorted(
            valid_data,
            key=lambda item: item[1]["temperature"],
            reverse=reverse
        )

    def average_humidity(self):
        humidity_values = [
            data["humidity"]
            for data in self.weather_data.values()
            if isinstance(data.get("humidity"), (int, float))
        ]

        if not humidity_values:
            return 0

        return sum(humidity_values) / len(humidity_values)

    def weather_report(self):
        print("\nWEATHER REPORT")
        print("=" * 50)

        for city, data in self.weather_data.items():
            print(
                f"{city}: "
                f"{data.get('temperature', 'N/A')}°C | "
                f"Humidity: {data.get('humidity', 'N/A')}% | "
                f"Condition: {data.get('condition', 'N/A')}"
            )


weather_data = {
    "Delhi": {
        "temperature": 34,
        "humidity": 65,
        "condition": "Sunny"
    },

    "Mumbai": {
        "temperature": 29,
        "humidity": 78,
        "condition": "Cloudy"
    },

    "Bangalore": {
        "temperature": 24,
        "humidity": 70,
        "condition": "Rainy"
    },

    "Jaipur": {
        "temperature": 37,
        "humidity": 45,
        "condition": "Sunny"
    },

    "Kolkata": {
        "temperature": 32,
        "humidity": 82,
        "condition": "Cloudy"
    }
}


analyzer = WeatherAnalyzer(weather_data)

analyzer.weather_report()

print(
    "\nAverage Temperature:",
    analyzer.average_temperature()
)

print(
    "Average Humidity:",
    analyzer.average_humidity()
)


hottest = analyzer.hottest_city()

if hottest:
    city, data = hottest
    print(
        f"\nHottest City: {city} "
        f"({data['temperature']}°C)"
    )


coldest = analyzer.coldest_city()

if coldest:
    city, data = coldest
    print(
        f"Coldest City: {city} "
        f"({data['temperature']}°C)"
    )


print("\nCities Above 30°C:")

for city in analyzer.cities_above_temperature(30):
    print(city)


print("\nCities Sorted by Temperature:")

for city, data in analyzer.sort_by_temperature():
    print(
        f"{city}: {data['temperature']}°C"
    )