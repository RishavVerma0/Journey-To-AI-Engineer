class EventManager:

    def __init__(self):
        self.listeners = {}

    def subscribe(self, event, callback):
        self.listeners.setdefault(event, []).append(callback)

    def emit(self, event, *args, **kwargs):
        for callback in self.listeners.get(event, []):
            callback(*args, **kwargs)


def user_registered(username):
    print(f"Welcome {username}!")


def send_email(username, email):
    print(f"Email sent to {email} for {username}")


def log_activity(username, **details):
    print(f"LOG: {username} -> {details}")


events = EventManager()

events.subscribe("registered", user_registered)
events.subscribe("registered", send_email)
events.subscribe("registered", log_activity)

events.emit(
    "registered",
    "Rishav",
    email="rishav@example.com",
    source="website"
)