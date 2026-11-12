import time
import uuid
import heapq
import threading

from enum import Enum
from datetime import datetime
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor


# -------------------------------
# Task Status
# -------------------------------

class TaskStatus(Enum):
    PENDING = "Pending"
    RUNNING = "Running"
    COMPLETED = "Completed"
    FAILED = "Failed"


# -------------------------------
# Custom Exceptions
# -------------------------------

class TaskNotFoundError(Exception):
    pass


# -------------------------------
# Abstract Task
# -------------------------------

class BaseTask(ABC):

    def __init__(self, name, priority=5, max_retries=3):
        self.task_id = str(uuid.uuid4())[:8]
        self.name = name
        self.priority = priority
        self.max_retries = max_retries
        self.retry_count = 0
        self.status = TaskStatus.PENDING
        self.created_at = datetime.now()

    @abstractmethod
    def execute(self):
        pass


# -------------------------------
# Concrete Tasks
# -------------------------------

class EmailTask(BaseTask):

    def __init__(self, recipient, priority=3):
        super().__init__("EmailTask", priority)
        self.recipient = recipient

    def execute(self): # type: ignore
        print(f"Sending email to {self.recipient}")
        time.sleep(2)
        return "Email sent successfully"


class DataProcessingTask(BaseTask):

    def __init__(self, records, priority=1):
        super().__init__("DataProcessingTask", priority)
        self.records = records

    def execute(self): # type: ignore

        print(f"Processing {len(self.records)} records")

        time.sleep(3)

        return {
            "processed_records": len(self.records),
            "status": "Success"
        }


class ReportTask(BaseTask):

    def __init__(self, report_name, priority=5):
        super().__init__("ReportTask", priority)
        self.report_name = report_name

    def execute(self): # type: ignore

        print(f"Generating report: {self.report_name}")

        time.sleep(1)

        return "Report generated successfully"


# -------------------------------
# Task Scheduler
# -------------------------------

class TaskScheduler:

    def __init__(self, max_workers=3):

        self.__tasks = {}
        self.__queue = []
        self.__lock = threading.Lock()

        self.executor = ThreadPoolExecutor(
            max_workers=max_workers
        )

    def submit_task(self, task):

        with self.__lock:

            self.__tasks[task.task_id] = task

            heapq.heappush(
                self.__queue,
                (task.priority, time.time(), task.task_id)
            )

        print(f"Task submitted: {task.name}")
        print(f"Task ID: {task.task_id}")

    def execute_task(self, task_id):

        task = self.__tasks.get(task_id)

        if not task:
            raise TaskNotFoundError(task_id)

        task.status = TaskStatus.RUNNING

        try:

            result = task.execute()

            task.status = TaskStatus.COMPLETED

            print(f"Task {task_id} completed!")
            print(f"Result: {result}")

        except Exception as error:

            task.retry_count += 1

            if task.retry_count <= task.max_retries:

                task.status = TaskStatus.PENDING

                print(
                    f"Retrying {task_id}: "
                    f"{task.retry_count}"
                )

                self.executor.submit(
                    self.execute_task, task_id
                )

            else:

                task.status = TaskStatus.FAILED

                print(f"Task failed: {error}")

    def run_scheduler(self):

        while self.__queue:

            with self.__lock:

                _, _, task_id = heapq.heappop(
                    self.__queue
                )

            self.executor.submit(
                self.execute_task, task_id
            )

        self.executor.shutdown(wait=True)

    def get_task_status(self, task_id):

        task = self.__tasks.get(task_id)

        if not task:
            raise TaskNotFoundError(task_id)

        return {
            "task_id": task.task_id,
            "name": task.name,
            "status": task.status.value,
            "retries": task.retry_count
        }


# -------------------------------
# Application
# -------------------------------

scheduler = TaskScheduler(max_workers=3)

# Creating tasks
email = EmailTask("rishav@example.com", priority=2)

data = DataProcessingTask(
    records=list(range(1000)),
    priority=1
)

report = ReportTask(
    "Monthly Revenue Report",
    priority=3
)

# Submitting tasks
scheduler.submit_task(email)
scheduler.submit_task(data)
scheduler.submit_task(report)

print("\nStarting Task Scheduler...\n")

scheduler.run_scheduler()

# Checking task statuses
print("\n========== TASK REPORT ==========")

for task in [email, data, report]:

    print(
        scheduler.get_task_status(task.task_id)
    )