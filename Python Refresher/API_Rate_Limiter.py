from time import time


class RateLimiter:
    def __init__(self, max_requests, window_seconds):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.__requests = {}

    def allow_request(self, user_id):
        current_time = time()

        if user_id not in self.__requests:
            self.__requests[user_id] = []

        # Keep only requests inside the current time window
        self.__requests[user_id] = [
            request_time
            for request_time in self.__requests[user_id]
            if current_time - request_time < self.window_seconds
        ]

        if len(self.__requests[user_id]) >= self.max_requests:
            return False

        self.__requests[user_id].append(current_time)

        return True


limiter = RateLimiter(max_requests=3, window_seconds=10)

for i in range(5):
    if limiter.allow_request("user_101"):
        print(f"Request {i + 1}: Allowed")
    else:
        print(f"Request {i + 1}: Rate Limited")