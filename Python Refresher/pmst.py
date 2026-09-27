from enum import Enum
from datetime import date, timedelta


# ============================================================
# ENUMS
# ============================================================

class TaskStatus(Enum):
    TODO = "Todo"
    IN_PROGRESS = "In Progress"
    BLOCKED = "Blocked"
    DONE = "Done"


class TaskPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class SprintStatus(Enum):
    PLANNED = "Planned"
    ACTIVE = "Active"
    COMPLETED = "Completed"


# ============================================================
# USER
# ============================================================

class TeamMember:

    def __init__(self, member_id, name, role):
        self.member_id = member_id
        self.name = name
        self.role = role

        self.tasks = []
        self.completed_points = 0

    def assign_task(self, task):
        if task not in self.tasks:
            self.tasks.append(task)

    def complete_task(self, task):
        if task in self.tasks and task.status != TaskStatus.DONE:
            task.status = TaskStatus.DONE
            self.completed_points += task.story_points

    def get_workload(self):
        active_tasks = [
            task for task in self.tasks
            if task.status in (
                TaskStatus.TODO,
                TaskStatus.IN_PROGRESS,
                TaskStatus.BLOCKED
            )
        ]

        return sum(task.story_points for task in active_tasks)

    def __str__(self):
        return f"{self.name} ({self.role})"


# ============================================================
# TASK
# ============================================================

class Task:

    def __init__(
        self,
        task_id,
        title,
        priority,
        story_points,
        due_date
    ):
        self.task_id = task_id
        self.title = title
        self.priority = priority
        self.story_points = story_points
        self.due_date = due_date

        self.status = TaskStatus.TODO
        self.assignee = None
        self.dependencies = []
        self.comments = []

    # --------------------------------------------------------
    # Dependency Management
    # --------------------------------------------------------

    def add_dependency(self, task):
        if task == self:
            raise ValueError("A task cannot depend on itself.")

        if task not in self.dependencies:
            self.dependencies.append(task)

    def dependencies_completed(self):

        return all(
            dependency.status == TaskStatus.DONE
            for dependency in self.dependencies
        )

    # --------------------------------------------------------
    # Assignment
    # --------------------------------------------------------

    def assign_to(self, member):

        if not self.dependencies_completed():
            print(
                f"Warning: '{self.title}' has incomplete dependencies."
            )

        self.assignee = member
        member.assign_task(self)

    # --------------------------------------------------------
    # Status Management
    # --------------------------------------------------------

    def start(self):

        if not self.dependencies_completed():
            self.status = TaskStatus.BLOCKED
            print(
                f"Task '{self.title}' is blocked because "
                f"dependencies are incomplete."
            )
            return

        self.status = TaskStatus.IN_PROGRESS

    def complete(self):

        if not self.dependencies_completed():
            raise ValueError(
                f"Cannot complete '{self.title}'. "
                f"Dependencies are incomplete."
            )

        self.status = TaskStatus.DONE

        if self.assignee:
            self.assignee.completed_points += self.story_points

    def block(self):
        self.status = TaskStatus.BLOCKED

    # --------------------------------------------------------
    # Comments
    # --------------------------------------------------------

    def add_comment(self, comment):
        self.comments.append(comment)

    # --------------------------------------------------------
    # Due Date
    # --------------------------------------------------------

    def is_overdue(self):

        if self.status == TaskStatus.DONE:
            return False

        return date.today() > self.due_date

    def __str__(self):
        assignee = (
            self.assignee.name
            if self.assignee
            else "Unassigned"
        )

        return (
            f"[{self.task_id}] {self.title} | "
            f"{self.status.value} | "
            f"{self.priority.name} | "
            f"{self.story_points} SP | "
            f"{assignee}"
        )


# ============================================================
# SPRINT
# ============================================================

class Sprint:

    def __init__(self, sprint_id, name, start_date, duration_days):

        self.sprint_id = sprint_id
        self.name = name
        self.start_date = start_date
        self.end_date = start_date + timedelta(days=duration_days)

        self.status = SprintStatus.PLANNED
        self.tasks = []

    def add_task(self, task):

        if task not in self.tasks:
            self.tasks.append(task)

    def start(self):

        if self.status != SprintStatus.PLANNED:
            raise ValueError("Sprint cannot be started.")

        self.status = SprintStatus.ACTIVE

    def complete(self):

        self.status = SprintStatus.COMPLETED

    def total_story_points(self):

        return sum(
            task.story_points
            for task in self.tasks
        )

    def completed_story_points(self):

        return sum(
            task.story_points
            for task in self.tasks
            if task.status == TaskStatus.DONE
        )

    def progress_percentage(self):

        total = self.total_story_points()

        if total == 0:
            return 0

        completed = self.completed_story_points()

        return round((completed / total) * 100, 2)

    def remaining_tasks(self):

        return [
            task
            for task in self.tasks
            if task.status != TaskStatus.DONE
        ]


# ============================================================
# PROJECT
# ============================================================

class Project:

    def __init__(self, project_id, name, manager):

        self.project_id = project_id
        self.name = name
        self.manager = manager

        self.members = []
        self.tasks = []
        self.sprints = []

    # --------------------------------------------------------
    # Team Management
    # --------------------------------------------------------

    def add_member(self, member):

        if member not in self.members:
            self.members.append(member)

    # --------------------------------------------------------
    # Task Management
    # --------------------------------------------------------

    def create_task(
        self,
        task_id,
        title,
        priority,
        story_points,
        due_date
    ):

        task = Task(
            task_id,
            title,
            priority,
            story_points,
            due_date
        )

        self.tasks.append(task)

        return task

    # --------------------------------------------------------
    # Sprint Management
    # --------------------------------------------------------

    def create_sprint(
        self,
        sprint_id,
        name,
        start_date,
        duration_days
    ):

        sprint = Sprint(
            sprint_id,
            name,
            start_date,
            duration_days
        )

        self.sprints.append(sprint)

        return sprint

    # --------------------------------------------------------
    # Smart Assignment
    # --------------------------------------------------------

    def auto_assign(self, task):

        if not self.members:
            raise ValueError("No team members available.")

        # Assign to member with lowest workload
        available_member = min(
            self.members,
            key=lambda member: member.get_workload()
        )

        task.assign_to(available_member)

        print(
            f"Task '{task.title}' automatically assigned to "
            f"{available_member.name}"
        )

    # --------------------------------------------------------
    # Search
    # --------------------------------------------------------

    def find_task(self, task_id):

        for task in self.tasks:
            if task.task_id == task_id:
                return task

        return None

    # --------------------------------------------------------
    # Project Statistics
    # --------------------------------------------------------

    def project_progress(self):

        if not self.tasks:
            return 0

        completed = sum(
            1
            for task in self.tasks
            if task.status == TaskStatus.DONE
        )

        return round(
            completed / len(self.tasks) * 100,
            2
        )

    def overdue_tasks(self):

        return [
            task
            for task in self.tasks
            if task.is_overdue()
        ]

    # --------------------------------------------------------
    # Priority Queue
    # --------------------------------------------------------

    def get_priority_tasks(self):

        return sorted(
            self.tasks,
            key=lambda task: (
                task.priority.value,
                task.story_points
            ),
            reverse=True
        )

    # --------------------------------------------------------
    # Dashboard
    # --------------------------------------------------------

    def dashboard(self):

        print("\n========== PROJECT DASHBOARD ==========")

        print(f"Project: {self.name}")
        print(f"Manager: {self.manager.name}")

        print(f"Total Tasks: {len(self.tasks)}")

        completed = sum(
            1
            for task in self.tasks
            if task.status == TaskStatus.DONE
        )

        blocked = sum(
            1
            for task in self.tasks
            if task.status == TaskStatus.BLOCKED
        )

        print(f"Completed: {completed}")
        print(f"Blocked: {blocked}")
        print(f"Progress: {self.project_progress()}%")

        print("\nTeam Workload:")

        for member in self.members:

            print(
                f"- {member.name}: "
                f"{member.get_workload()} active SP"
            )


# ============================================================
# PROJECT MANAGEMENT SYSTEM
# ============================================================

class ProjectManagementSystem:

    def __init__(self):

        self.projects = {}
        self.members = {}

    # --------------------------------------------------------
    # Register Member
    # --------------------------------------------------------

    def register_member(self, member):

        if member.member_id in self.members:
            raise ValueError("Member already exists.")

        self.members[member.member_id] = member

    # --------------------------------------------------------
    # Register Project
    # --------------------------------------------------------

    def create_project(self, project):

        if project.project_id in self.projects:
            raise ValueError("Project already exists.")

        self.projects[project.project_id] = project

    # --------------------------------------------------------
    # Assign Specific Member
    # --------------------------------------------------------

    def assign_task(self, project_id, task_id, member_id):

        project = self.projects[project_id]
        task = project.find_task(task_id)
        member = self.members[member_id]

        if task is None:
            raise ValueError("Task not found.")

        task.assign_to(member)

    # --------------------------------------------------------
    # Complete Task
    # --------------------------------------------------------

    def complete_task(self, project_id, task_id):

        project = self.projects[project_id]
        task = project.find_task(task_id)

        if task is None:
            raise ValueError("Task not found.")

        task.complete()

    # --------------------------------------------------------
    # Print Team Report
    # --------------------------------------------------------

    def team_report(self):

        print("\n========== TEAM REPORT ==========")

        for member in self.members.values():

            print(f"\nMember: {member.name}")
            print(f"Role: {member.role}")
            print(f"Active Workload: {member.get_workload()} SP")
            print(f"Completed Points: {member.completed_points}")

            print("Tasks:")

            for task in member.tasks:
                print(
                    f"  - {task.title} "
                    f"({task.status.value})"
                )


# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":

    system = ProjectManagementSystem()

    # --------------------------------------------------------
    # Create Team
    # --------------------------------------------------------

    manager = TeamMember(
        "E001",
        "Rishav",
        "Project Manager"
    )

    backend = TeamMember(
        "E002",
        "Aman",
        "Backend Developer"
    )

    frontend = TeamMember(
        "E003",
        "Priya",
        "Frontend Developer"
    )

    ai_engineer = TeamMember(
        "E004",
        "Rahul",
        "AI Engineer"
    )

    system.register_member(manager)
    system.register_member(backend)
    system.register_member(frontend)
    system.register_member(ai_engineer)

    # --------------------------------------------------------
    # Create Project
    # --------------------------------------------------------

    project = Project(
        "P001",
        "AI Customer Support Platform",
        manager
    )

    project.add_member(backend)
    project.add_member(frontend)
    project.add_member(ai_engineer)

    system.create_project(project)

    # --------------------------------------------------------
    # Create Tasks
    # --------------------------------------------------------

    api_task = project.create_task(
        "T001",
        "Build Authentication API",
        TaskPriority.HIGH,
        5,
        date.today() + timedelta(days=5)
    )

    database_task = project.create_task(
        "T002",
        "Design Customer Database",
        TaskPriority.HIGH,
        8,
        date.today() + timedelta(days=4)
    )

    rag_task = project.create_task(
        "T003",
        "Implement RAG Pipeline",
        TaskPriority.CRITICAL,
        13,
        date.today() + timedelta(days=10)
    )

    chatbot_task = project.create_task(
        "T004",
        "Build Customer Chatbot",
        TaskPriority.CRITICAL,
        8,
        date.today() + timedelta(days=12)
    )

    testing_task = project.create_task(
        "T005",
        "Integration Testing",
        TaskPriority.MEDIUM,
        5,
        date.today() + timedelta(days=15)
    )

    # --------------------------------------------------------
    # Dependencies
    # --------------------------------------------------------

    rag_task.add_dependency(database_task)

    chatbot_task.add_dependency(rag_task)

    testing_task.add_dependency(
        chatbot_task
    )

    # --------------------------------------------------------
    # Explicit Assignment
    # --------------------------------------------------------

    api_task.assign_to(backend)

    database_task.assign_to(backend)

    rag_task.assign_to(ai_engineer)

    # --------------------------------------------------------
    # Automatic Assignment
    # --------------------------------------------------------

    project.auto_assign(chatbot_task)
    project.auto_assign(testing_task)

    # --------------------------------------------------------
    # Create Sprint
    # --------------------------------------------------------

    sprint = project.create_sprint(
        "S001",
        "AI Platform Sprint 1",
        date.today(),
        14
    )

    sprint.add_task(api_task)
    sprint.add_task(database_task)
    sprint.add_task(rag_task)
    sprint.add_task(chatbot_task)
    sprint.add_task(testing_task)

    sprint.start()

    # --------------------------------------------------------
    # Work Progress
    # --------------------------------------------------------

    api_task.start()
    api_task.complete()

    database_task.start()
    database_task.complete()

    # RAG can now start because database is complete
    rag_task.start()

    # Complete RAG
    rag_task.complete()

    # Chatbot dependency is now complete
    chatbot_task.start()
    chatbot_task.complete()

    # Testing can now start
    testing_task.start()
    testing_task.complete()

    sprint.complete()

    # --------------------------------------------------------
    # Print Tasks
    # --------------------------------------------------------

    print("\n========== ALL TASKS ==========")

    for task in project.tasks:
        print(task)

    # --------------------------------------------------------
    # Sprint Report
    # --------------------------------------------------------

    print("\n========== SPRINT REPORT ==========")

    print(f"Sprint: {sprint.name}")
    print(f"Status: {sprint.status.value}")

    print(
        f"Total Story Points: "
        f"{sprint.total_story_points()}"
    )

    print(
        f"Completed Story Points: "
        f"{sprint.completed_story_points()}"
    )

    print(
        f"Progress: "
        f"{sprint.progress_percentage()}%"
    )

    # --------------------------------------------------------
    # Priority Queue
    # --------------------------------------------------------

    print("\n========== PRIORITY QUEUE ==========")

    for task in project.get_priority_tasks():
        print(
            f"{task.priority.name:8} | "
            f"{task.story_points:2} SP | "
            f"{task.title}"
        )

    # --------------------------------------------------------
    # Dashboard
    # --------------------------------------------------------

    project.dashboard()

    # --------------------------------------------------------
    # Team Report
    # --------------------------------------------------------

    system.team_report()