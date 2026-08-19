class TaskManager:
    def __init__(self):
        self.tasks = {}

    def add_task(self, task_id, task):
        self.tasks[task_id] = {
            "task": task,
            "completed": False
        }

    def complete_task(self, task_id):
        if task_id in self.tasks:
            self.tasks[task_id]["completed"] = True

    def pending_tasks(self):
        return [
            task["task"]
            for task in self.tasks.values()
            if not task["completed"]
        ]


manager = TaskManager()

manager.add_task(1, "Learn Python")
manager.add_task(2, "Practice SQL")
manager.add_task(3, "Build RAG project")

manager.complete_task(1)

print("Pending tasks:", manager.pending_tasks())