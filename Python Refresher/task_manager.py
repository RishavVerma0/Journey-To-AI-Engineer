from abc import ABC, abstractmethod


class Task(ABC):
    def __init__(self, title):
        self.title = title
        self.completed = False

    @abstractmethod
    def complete(self):
        pass

    def status(self):
        return "Completed" if self.completed else "Pending"


class NormalTask(Task):
    def complete(self):
        self.completed = True
        print(f"Task completed: {self.title}")


class UrgentTask(Task):
    def complete(self):
        self.completed = True
        print(f"URGENT task completed: {self.title}")


class RecurringTask(Task):
    def __init__(self, title, repetitions):
        super().__init__(title)
        self.repetitions = repetitions

    def complete(self):
        if self.repetitions > 0:
            self.repetitions -= 1

        if self.repetitions == 0:
            self.completed = True

        print(
            f"{self.title} | "
            f"Remaining: {self.repetitions}"
        )


tasks = [
    NormalTask("Learn Python OOP"),
    UrgentTask("Submit project"),
    RecurringTask("Practice LeetCode", 3)
]

for task in tasks:
    task.complete()
    print("Status:", task.status())
    print("-" * 30)