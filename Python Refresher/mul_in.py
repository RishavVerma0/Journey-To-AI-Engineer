class Logger:
    def __init__(self):
        print("Logger initialized")
        super().__init__()

    def log(self, message):
        print(f"[LOG] {message}")


class Database:
    def __init__(self):
        print("Database initialized")
        super().__init__()

    def save(self, data):
        print(f"Saving {data} to database")


class Cache:
    def __init__(self):
        print("Cache initialized")
        super().__init__()

    def save(self, data):
        print(f"Caching {data}")
        super().save(data) # type: ignore


class UserService(Cache, Database, Logger):
    def __init__(self):
        print("UserService initialized")
        super().__init__()

    def create_user(self, name):
        self.log(f"Creating user: {name}")
        self.save({"name": name})


service = UserService()

print("\nMRO:")
for cls in UserService.mro():
    print(cls.__name__)

print("\nOperation:")
service.create_user("Rishav")