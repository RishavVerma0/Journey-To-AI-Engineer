from datetime import datetime


class APITracker:
    def __init__(self):
        self.requests = []

    def log_request(self, endpoint, method, status_code, response_time):
        request = {
            "endpoint": endpoint,
            "method": method,
            "status_code": status_code,
            "response_time": response_time,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        }

        self.requests.append(request)

    def get_failed_requests(self):
        return [
            request for request in self.requests
            if request["status_code"] >= 400
        ]

    def average_response_time(self):
        if not self.requests:
            return 0

        total = sum(r["response_time"] for r in self.requests)
        return total / len(self.requests)

    def show_report(self):
        print(f"Total Requests: {len(self.requests)}")
        print(f"Failed Requests: {len(self.get_failed_requests())}")
        print(f"Average Response Time: {self.average_response_time():.2f} ms")

        for request in self.get_failed_requests():
            print(
                f"{request['method']} {request['endpoint']} "
                f"-> {request['status_code']}"
            )


tracker = APITracker()

tracker.log_request("/users", "GET", 200, 120)
tracker.log_request("/login", "POST", 401, 85)
tracker.log_request("/products", "GET", 200, 150)
tracker.log_request("/orders", "POST", 500, 300)

tracker.show_report()