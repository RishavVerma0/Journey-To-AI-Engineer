class URLMonitor:
    def __init__(self):
        self.urls = {}

    def add_url(self, name, url):
        self.urls[name] = {
            "url": url,
            "status": "Unknown",
            "checks": 0
        }

    def record_check(self, name, is_online):
        if name not in self.urls:
            print("URL not found")
            return

        self.urls[name]["status"] = (
            "Online" if is_online else "Offline"
        )
        self.urls[name]["checks"] += 1

    def show_report(self):
        for name, details in self.urls.items():
            print(f"\nService: {name}")
            print(f"URL: {details['url']}")
            print(f"Status: {details['status']}")
            print(f"Total Checks: {details['checks']}")

    def get_offline_services(self):
        return [
            name for name, details in self.urls.items()
            if details["status"] == "Offline"
        ]


monitor = URLMonitor()

monitor.add_url("Google", "https://google.com")
monitor.add_url("GitHub", "https://github.com")
monitor.add_url("My API", "https://api.example.com")

# Simulated results; no actual network requests are made.
monitor.record_check("Google", True)
monitor.record_check("GitHub", True)
monitor.record_check("My API", False)

monitor.show_report()

print("\nOffline Services:", monitor.get_offline_services())