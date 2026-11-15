import time
import uuid
import threading

from abc import ABC, abstractmethod
from collections import defaultdict, deque
from datetime import datetime


# -------------------------------
# Custom Exceptions
# -------------------------------

class RateLimitExceeded(Exception):
    pass


class InvalidAPIKey(Exception):
    pass


# -------------------------------
# Abstract Rate Limiting Strategy
# -------------------------------

class RateLimitStrategy(ABC):

    @abstractmethod
    def allow_request(self, client_id):
        pass


# -------------------------------
# Sliding Window Rate Limiter
# -------------------------------

class SlidingWindowLimiter(RateLimitStrategy):

    def __init__(self, max_requests, window_seconds):

        self.max_requests = max_requests
        self.window_seconds = window_seconds

        self.requests = defaultdict(deque)
        self.lock = threading.Lock()

    def allow_request(self, client_id): # type: ignore

        with self.lock:

            current_time = time.time()

            request_queue = self.requests[client_id]

            # Remove expired requests
            while (
                request_queue and
                current_time - request_queue[0] >= self.window_seconds
            ):
                request_queue.popleft()

            if len(request_queue) >= self.max_requests:
                return False

            request_queue.append(current_time)

            return True


# -------------------------------
# API Client
# -------------------------------

class APIClient:

    def __init__(self, name, api_key, subscription):

        self.client_id = str(uuid.uuid4())[:8]

        self.name = name
        self.__api_key = api_key

        self.subscription = subscription

        self.total_requests = 0
        self.blocked = False

    def validate_key(self, key):
        return self.__api_key == key

    def increment_requests(self):
        self.total_requests += 1


# -------------------------------
# Request Logger
# -------------------------------

class RequestLogger:

    def __init__(self):
        self.logs = []

    def log(self, client, status):

        self.logs.append({
            "client": client.name,
            "status": status,
            "timestamp": datetime.now()
        })

    def display_logs(self):

        for log in self.logs:
            print(log)


# -------------------------------
# API Gateway
# -------------------------------

class APIGateway:

    def __init__(self):

        self.clients = {}

        self.limiters = {
            "Free": SlidingWindowLimiter(5, 10),
            "Pro": SlidingWindowLimiter(20, 10),
            "Enterprise": SlidingWindowLimiter(100, 10)
        }

        self.logger = RequestLogger()

    def register_client(self, client):

        self.clients[client.client_id] = client

        print(
            f"Registered {client.name} "
            f"with {client.subscription} subscription."
        )

    def process_request(self, client_id, api_key):

        client = self.clients.get(client_id)

        if not client:
            raise InvalidAPIKey("Unknown API client.")

        if not client.validate_key(api_key):
            raise InvalidAPIKey("Invalid API key.")

        if client.blocked:
            self.logger.log(client, "Blocked")
            raise RateLimitExceeded("Client is blocked.")

        limiter = self.limiters.get(client.subscription)

        if not limiter:
            raise ValueError("Invalid subscription plan.")

        if not limiter.allow_request(client_id):

            self.logger.log(client, "Rate Limited")

            raise RateLimitExceeded(
                f"{client.name} exceeded request quota."
            )

        client.increment_requests()

        self.logger.log(client, "Success")

        return {
            "message": "Request processed successfully",
            "client": client.name,
            "total_requests": client.total_requests
        }


# -------------------------------
# Application
# -------------------------------

gateway = APIGateway()

# Register clients
client1 = APIClient(
    "Rishav",
    "API_KEY_101",
    "Free"
)

client2 = APIClient(
    "Rahul",
    "API_KEY_202",
    "Pro"
)

gateway.register_client(client1)
gateway.register_client(client2)


# Simulate incoming requests
print("\n----- API Request Simulation -----")

for i in range(7):

    try:

        response = gateway.process_request(
            client1.client_id,
            "API_KEY_101"
        )

        print(f"Request {i + 1}: {response}")

    except (RateLimitExceeded, InvalidAPIKey) as error:

        print(f"Request {i + 1}: {error}")


# Display request logs
print("\n----- API Request Logs -----")

gateway.logger.display_logs()