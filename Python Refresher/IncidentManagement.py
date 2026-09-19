from datetime import datetime, timedelta
from enum import Enum


# ---------------------------------------------------------
# ENUMS
# ---------------------------------------------------------

class Priority(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class IncidentStatus(Enum):
    OPEN = "Open"
    ASSIGNED = "Assigned"
    IN_PROGRESS = "In Progress"
    RESOLVED = "Resolved"
    CLOSED = "Closed"


# ---------------------------------------------------------
# USER
# ---------------------------------------------------------

class User:

    def __init__(self, user_id, name, department):
        self.user_id = user_id
        self.name = name
        self.department = department

    def __str__(self):
        return f"{self.name} ({self.department})"


# ---------------------------------------------------------
# SUPPORT AGENT
# ---------------------------------------------------------

class SupportAgent(User):

    def __init__(self, user_id, name, department, skills):
        super().__init__(user_id, name, department)

        self.skills = set(skills)
        self.active_incidents = []
        self.max_incidents = 3

    def can_handle(self, required_skill):

        return (
            required_skill in self.skills
            and len(self.active_incidents) < self.max_incidents
        )

    def assign_incident(self, incident):

        if len(self.active_incidents) >= self.max_incidents:
            raise Exception(
                f"{self.name} cannot accept more incidents."
            )

        self.active_incidents.append(incident)

    def remove_incident(self, incident):

        if incident in self.active_incidents:
            self.active_incidents.remove(incident)

    def __str__(self):

        return (
            f"{self.name} | "
            f"Skills: {', '.join(self.skills)} | "
            f"Active: {len(self.active_incidents)}"
        )


# ---------------------------------------------------------
# SLA POLICY
# ---------------------------------------------------------

class SLAPolicy:

    SLA_HOURS = {
        Priority.CRITICAL: 2,
        Priority.HIGH: 4,
        Priority.MEDIUM: 8,
        Priority.LOW: 24
    }

    @classmethod
    def get_deadline(cls, priority, created_at):

        hours = cls.SLA_HOURS[priority]

        return created_at + timedelta(hours=hours)

    @classmethod
    def is_breached(cls, incident):

        return datetime.now() > incident.sla_deadline


# ---------------------------------------------------------
# INCIDENT
# ---------------------------------------------------------

class Incident:

    counter = 1000

    def __init__(
        self,
        title,
        description,
        reported_by,
        priority,
        required_skill
    ):

        Incident.counter += 1

        self.incident_id = f"INC{Incident.counter}"

        self.title = title
        self.description = description
        self.reported_by = reported_by

        self.priority = priority
        self.required_skill = required_skill

        self.status = IncidentStatus.OPEN

        self.created_at = datetime.now()

        self.sla_deadline = SLAPolicy.get_deadline(
            priority,
            self.created_at
        )

        self.assigned_agent = None

        self.comments = []

        self.resolution = None

    # -----------------------------------------------------
    # ASSIGNMENT
    # -----------------------------------------------------

    def assign_to(self, agent):

        if not agent.can_handle(self.required_skill):

            raise Exception(
                f"{agent.name} does not have required skill "
                f"or has reached maximum workload."
            )

        self.assigned_agent = agent

        agent.assign_incident(self)

        self.status = IncidentStatus.ASSIGNED

        self.add_comment(
            f"Incident assigned to {agent.name}"
        )

    # -----------------------------------------------------
    # START WORK
    # -----------------------------------------------------

    def start_work(self):

        if self.status != IncidentStatus.ASSIGNED:

            raise Exception(
                "Incident must be assigned before work starts."
            )

        self.status = IncidentStatus.IN_PROGRESS

        assert self.assigned_agent is not None
        self.add_comment(
            f"Work started by {self.assigned_agent.name}"
        )

    # -----------------------------------------------------
    # RESOLVE
    # -----------------------------------------------------

    def resolve(self, resolution):

        if self.status != IncidentStatus.IN_PROGRESS:

            raise Exception(
                "Incident must be in progress before resolution."
            )

        self.resolution = resolution

        self.status = IncidentStatus.RESOLVED

        if self.assigned_agent:
            self.assigned_agent.remove_incident(self)

        self.add_comment(
            f"Incident resolved: {resolution}"
        )

    # -----------------------------------------------------
    # CLOSE
    # -----------------------------------------------------

    def close(self):

        if self.status != IncidentStatus.RESOLVED:

            raise Exception(
                "Only resolved incidents can be closed."
            )

        self.status = IncidentStatus.CLOSED

        self.add_comment("Incident closed by system.")

    # -----------------------------------------------------
    # COMMENTS
    # -----------------------------------------------------

    def add_comment(self, message):

        self.comments.append({
            "time": datetime.now(),
            "message": message
        })

    # -----------------------------------------------------
    # SLA
    # -----------------------------------------------------

    def sla_status(self):

        if SLAPolicy.is_breached(self):

            return "SLA BREACHED"

        remaining = self.sla_deadline - datetime.now()

        return f"SLA remaining: {remaining}"

    # -----------------------------------------------------
    # DISPLAY
    # -----------------------------------------------------

    def display(self):

        print("\n" + "=" * 60)

        print(f"Incident ID : {self.incident_id}")
        print(f"Title       : {self.title}")
        print(f"Priority    : {self.priority.value}")
        print(f"Status      : {self.status.value}")
        print(f"Skill       : {self.required_skill}")

        if self.assigned_agent:

            print(
                f"Assigned To : "
                f"{self.assigned_agent.name}"
            )

        else:

            print("Assigned To : Unassigned")

        print(f"SLA         : {self.sla_status()}")

        if self.resolution:

            print(f"Resolution  : {self.resolution}")

        print("=" * 60)


# ---------------------------------------------------------
# INCIDENT MANAGER
# ---------------------------------------------------------

class IncidentManager:

    def __init__(self):

        self.incidents = {}
        self.agents = {}

    # -----------------------------------------------------
    # REGISTER AGENT
    # -----------------------------------------------------

    def register_agent(self, agent):

        self.agents[agent.user_id] = agent

    # -----------------------------------------------------
    # CREATE INCIDENT
    # -----------------------------------------------------

    def create_incident(
        self,
        title,
        description,
        user,
        priority,
        skill
    ):

        incident = Incident(
            title,
            description,
            user,
            priority,
            skill
        )

        self.incidents[incident.incident_id] = incident

        return incident

    # -----------------------------------------------------
    # AUTO ASSIGN
    # -----------------------------------------------------

    def auto_assign(self, incident):

        suitable_agents = [

            agent

            for agent in self.agents.values()

            if agent.can_handle(incident.required_skill)

        ]

        if not suitable_agents:

            print(
                f"No available agent for "
                f"{incident.incident_id}"
            )

            return None

        # Choose least-loaded agent

        selected_agent = min(
            suitable_agents,
            key=lambda agent: len(agent.active_incidents)
        )

        incident.assign_to(selected_agent)

        return selected_agent

    # -----------------------------------------------------
    # SEARCH
    # -----------------------------------------------------

    def search(self, keyword):

        results = []

        for incident in self.incidents.values():

            if (
                keyword.lower() in incident.title.lower()
                or keyword.lower() in incident.description.lower()
            ):
                results.append(incident)

        return results

    # -----------------------------------------------------
    # DISPLAY ALL
    # -----------------------------------------------------

    def display_all(self):

        for incident in self.incidents.values():

            incident.display()


# ---------------------------------------------------------
# DEMO
# ---------------------------------------------------------

manager = IncidentManager()


# Users

user1 = User(
    "U101",
    "Rahul",
    "Finance"
)

user2 = User(
    "U102",
    "Ankit",
    "HR"
)


# Support agents

agent1 = SupportAgent(
    "A101",
    "Amit",
    "IT Support",
    ["Network", "Hardware"]
)

agent2 = SupportAgent(
    "A102",
    "Priya",
    "IT Support",
    ["Java", "Database", "Linux"]
)

agent3 = SupportAgent(
    "A103",
    "Rohit",
    "IT Support",
    ["Python", "Cloud", "Linux"]
)


manager.register_agent(agent1)
manager.register_agent(agent2)
manager.register_agent(agent3)


# ---------------------------------------------------------
# CREATE INCIDENTS
# ---------------------------------------------------------

incident1 = manager.create_incident(
    title="Application server is down",
    description="Production Java application is not responding",
    user=user1,
    priority=Priority.CRITICAL,
    skill="Java"
)


incident2 = manager.create_incident(
    title="Database connection failure",
    description="Application cannot connect to database",
    user=user2,
    priority=Priority.HIGH,
    skill="Database"
)


incident3 = manager.create_incident(
    title="VPN connectivity issue",
    description="Unable to connect to corporate VPN",
    user=user1,
    priority=Priority.MEDIUM,
    skill="Network"
)


# ---------------------------------------------------------
# AUTO ASSIGN
# ---------------------------------------------------------

manager.auto_assign(incident1)
manager.auto_assign(incident2)
manager.auto_assign(incident3)


# ---------------------------------------------------------
# PROCESS INCIDENT
# ---------------------------------------------------------

incident1.start_work()

incident1.resolve(
    "Restarted application server and fixed configuration."
)

incident1.close()


# ---------------------------------------------------------
# DISPLAY
# ---------------------------------------------------------

manager.display_all()


# ---------------------------------------------------------
# SEARCH
# ---------------------------------------------------------

print("\nSEARCH RESULTS")

results = manager.search("database")

for incident in results:

    print(
        incident.incident_id,
        incident.title
    )