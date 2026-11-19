import uuid
import time
import threading

from abc import ABC, abstractmethod
from enum import Enum
from concurrent.futures import ThreadPoolExecutor


# --------------------------------
# Workflow States
# --------------------------------

class TaskStatus(Enum):
    PENDING = "Pending"
    RUNNING = "Running"
    COMPLETED = "Completed"
    FAILED = "Failed"


# --------------------------------
# Custom Exceptions
# --------------------------------

class DependencyError(Exception):
    pass


class WorkflowExecutionError(Exception):
    pass


# --------------------------------
# Abstract Task
# --------------------------------

class BaseTask(ABC):

    def __init__(self, name, dependencies=None, max_retries=2):

        self.task_id = str(uuid.uuid4())[:8]
        self.name = name

        self.dependencies = dependencies or []

        self.max_retries = max_retries
        self.retry_count = 0

        self.status = TaskStatus.PENDING
        self.result = None

    @abstractmethod
    def execute(self, context):
        pass


# --------------------------------
# Data Collection Task
# --------------------------------

class DataCollectionTask(BaseTask):

    def execute(self, context): # type: ignore

        print(f"[COLLECT] Executing {self.name}")

        time.sleep(2)

        data = {
            "users": 1500,
            "revenue": 75000,
            "active_sessions": 420
        }

        context[self.name] = data

        return data


# --------------------------------
# Data Analysis Task
# --------------------------------

class DataAnalysisTask(BaseTask):

    def execute(self, context): # type: ignore

        print(f"[ANALYSIS] Executing {self.name}")

        collected_data = context.get("collect_data")

        if not collected_data:
            raise ValueError("Required data unavailable")

        time.sleep(1)

        result = {
            "revenue_per_user":
                collected_data["revenue"] /
                collected_data["users"],

            "engagement":
                collected_data["active_sessions"] /
                collected_data["users"] * 100
        }

        context[self.name] = result

        return result


# --------------------------------
# Report Generation Task
# --------------------------------

class ReportTask(BaseTask):

    def execute(self, context): # type: ignore

        print(f"[REPORT] Executing {self.name}")

        analysis = context.get("analyze_data")

        if not analysis:
            raise ValueError("Analysis unavailable")

        report = (
            f"Revenue per User: "
            f"{analysis['revenue_per_user']}\n"

            f"Engagement: "
            f"{analysis['engagement']}%"
        )

        context[self.name] = report

        return report


# --------------------------------
# Workflow Engine
# --------------------------------

class WorkflowEngine:

    def __init__(self, max_workers=3):

        self.tasks = {}
        self.context = {}

        self.executor = ThreadPoolExecutor(
            max_workers=max_workers
        )

        self.lock = threading.Lock()

    def add_task(self, task):

        if task.name in self.tasks:
            raise ValueError("Duplicate task name")

        self.tasks[task.name] = task

    def validate_dependencies(self):

        for task in self.tasks.values():

            for dependency in task.dependencies:

                if dependency not in self.tasks:
                    raise DependencyError(
                        f"Missing dependency: {dependency}"
                    )

        # Detect circular dependencies
        visited = set()
        active = set()

        def detect_cycle(name):

            if name in active:
                raise DependencyError(
                    "Circular dependency detected"
                )

            if name in visited:
                return

            active.add(name)

            for dependency in self.tasks[name].dependencies:
                detect_cycle(dependency)

            active.remove(name)
            visited.add(name)

        for name in self.tasks:
            detect_cycle(name)

    def execute_task(self, task):

        with self.lock:
            task.status = TaskStatus.RUNNING

        try:

            result = task.execute(self.context)

            with self.lock:
                task.result = result
                task.status = TaskStatus.COMPLETED

            print(f"[SUCCESS] {task.name}")

        except Exception as error:

            task.retry_count += 1

            print(
                f"[ERROR] {task.name}: {error}"
            )

            with self.lock:

                if task.retry_count <= task.max_retries:
                    task.status = TaskStatus.PENDING

                else:
                    task.status = TaskStatus.FAILED

    def run(self):

        self.validate_dependencies()

        print("\nStarting Workflow Execution...\n")

        while True:

            completed = {
                name for name, task in self.tasks.items()
                if task.status == TaskStatus.COMPLETED
            }

            pending_tasks = [
                task for task in self.tasks.values()
                if task.status == TaskStatus.PENDING
                and all(
                    dependency in completed
                    for dependency in task.dependencies
                )
            ]

            if not pending_tasks:
                break

            futures = [
                self.executor.submit(
                    self.execute_task,
                    task
                )
                for task in pending_tasks
            ]

            for future in futures:
                future.result()

            failed_tasks = [
                task for task in self.tasks.values()
                if task.status == TaskStatus.FAILED
            ]

            if failed_tasks:
                raise WorkflowExecutionError(
                    "Workflow stopped because a task failed."
                )

        self.executor.shutdown(wait=True)

        if not all(
            task.status == TaskStatus.COMPLETED
            for task in self.tasks.values()
        ):
            raise WorkflowExecutionError(
                "Workflow contains blocked tasks."
            )

        print("\nWorkflow Completed Successfully!")

    def execution_report(self):

        print("\n========== EXECUTION REPORT ==========")

        for task in self.tasks.values():

            print(f"\nTask: {task.name}")
            print(f"Status: {task.status.value}")
            print(f"Retries: {task.retry_count}")
            print(f"Result: {task.result}")


# --------------------------------
# Application
# --------------------------------

workflow = WorkflowEngine(max_workers=3)


# Define Tasks

collect = DataCollectionTask(
    name="collect_data"
)

analyze = DataAnalysisTask(
    name="analyze_data",
    dependencies=["collect_data"]
)

generate_report = ReportTask(
    name="generate_report",
    dependencies=["analyze_data"]
)


# Register Tasks

workflow.add_task(collect)
workflow.add_task(analyze)
workflow.add_task(generate_report)


# Execute Workflow

try:

    workflow.run()

    workflow.execution_report()

except (DependencyError, WorkflowExecutionError) as error:

    print(f"Workflow Error: {error}")