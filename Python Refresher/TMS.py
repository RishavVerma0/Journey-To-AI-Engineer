from datetime import datetime


class Task:
    def __init__(
        self,
        task_id,
        title,
        priority,
        deadline
    ):
        self.task_id = task_id
        self.title = title
        self.priority = priority
        self.deadline = datetime.strptime(
            deadline,
            "%Y-%m-%d"
        )
        self.completed = False

    def mark_completed(self):
        self.completed = True

    def is_overdue(self):
        current_date = datetime.now()

        return (
            not self.completed
            and self.deadline < current_date
        )

    def display_task(self):
        status = (
            "Completed"
            if self.completed
            else "Pending"
        )

        print("-" * 45)
        print(f"Task ID: {self.task_id}")
        print(f"Title: {self.title}")
        print(f"Priority: {self.priority}")
        print(
            f"Deadline: "
            f"{self.deadline.strftime('%Y-%m-%d')}"
        )
        print(f"Status: {status}")


class TaskManager:
    def __init__(self):
        self.tasks = {}

    def add_task(self, task):
        if task.task_id in self.tasks:
            raise ValueError("Task already exists")

        self.tasks[task.task_id] = task

        print("Task added successfully")

    def complete_task(self, task_id):
        if task_id not in self.tasks:
            raise ValueError("Task not found")

        self.tasks[task_id].mark_completed()

        print("Task marked as completed")

    def display_all_tasks(self):
        if not self.tasks:
            print("No tasks available")
            return

        for task in self.tasks.values():
            task.display_task()

    def show_pending_tasks(self):
        print("\nPENDING TASKS")

        for task in self.tasks.values():
            if not task.completed:
                task.display_task()

    def show_completed_tasks(self):
        print("\nCOMPLETED TASKS")

        for task in self.tasks.values():
            if task.completed:
                task.display_task()

    def show_overdue_tasks(self):
        print("\nOVERDUE TASKS")

        overdue_found = False

        for task in self.tasks.values():
            if task.is_overdue():
                task.display_task()
                overdue_found = True

        if not overdue_found:
            print("No overdue tasks")

    def sort_by_priority(self):
        priority_order = {
            "High": 1,
            "Medium": 2,
            "Low": 3
        }

        sorted_tasks = sorted(
            self.tasks.values(),
            key=lambda task: priority_order[
                task.priority
            ]
        )

        return sorted_tasks


manager = TaskManager()

task1 = Task(
    1,
    "Complete Python Project",
    "High",
    "2026-08-20"
)

task2 = Task(
    2,
    "Learn Pandas",
    "Medium",
    "2026-09-10"
)

task3 = Task(
    3,
    "Practice LeetCode",
    "High",
    "2026-09-01"
)

task4 = Task(
    4,
    "Read Documentation",
    "Low",
    "2026-10-01"
)

manager.add_task(task1)
manager.add_task(task2)
manager.add_task(task3)
manager.add_task(task4)

manager.complete_task(2)

manager.show_pending_tasks()

manager.show_completed_tasks()

manager.show_overdue_tasks()

print("\nTASKS SORTED BY PRIORITY")

sorted_tasks = manager.sort_by_priority()

for task in sorted_tasks:
    task.display_task()