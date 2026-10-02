class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append({
            "name": task,
            "completed": False
        })

    def complete_task(self, task_name):
        for task in self.tasks:
            if task["name"] == task_name:
                task["completed"] = True

    def show_tasks(self):
        for task in self.tasks:
            status = "Done" if task["completed"] else "Pending"
            print(f"{task['name']} - {status}")


manager = TaskManager()

manager.add_task("Learn Python")
manager.add_task("Practice Git")
manager.add_task("Build RAG project")

manager.complete_task("Learn Python")

manager.show_tasks()