import threading
import queue
import time
import random


class TaskQueue:
    def __init__(self, workers=3):
        self.tasks = queue.Queue()
        self.workers = workers
        self.threads = []

    def add_task(self, task):
        self.tasks.put(task)

    def worker(self, worker_id):
        while True:
            task = self.tasks.get()

            if task is None:
                self.tasks.task_done()
                break

            print(f"Worker {worker_id} processing: {task}")

            time.sleep(random.uniform(0.5, 1.5))

            print(f"Worker {worker_id} completed: {task}")

            self.tasks.task_done()

    def start(self):
        for i in range(self.workers):
            thread = threading.Thread(
                target=self.worker,
                args=(i + 1,)
            )

            thread.start()
            self.threads.append(thread)

    def shutdown(self):
        self.tasks.join()

        for _ in range(self.workers):
            self.tasks.put(None)

        for thread in self.threads:
            thread.join()


task_queue = TaskQueue(workers=3)

task_queue.start()

for i in range(10):
    task_queue.add_task(f"Task-{i + 1}")

task_queue.shutdown()

print("All tasks completed.")