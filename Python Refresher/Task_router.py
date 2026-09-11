class Task:
    def __init__(self, query):
        self.query = query


class Agent:
    def __init__(self, name):
        self.name = name

    def can_handle(self, task):
        raise NotImplementedError

    def execute(self, task):
        raise NotImplementedError


class CodingAgent(Agent):
    def can_handle(self, task):
        keywords = ["code", "python", "bug", "program"]

        return any(
            keyword in task.query.lower()
            for keyword in keywords
        )

    def execute(self, task):
        return f"{self.name} is solving the coding task."


class ResearchAgent(Agent):
    def can_handle(self, task):
        keywords = ["research", "find", "search", "explain"]

        return any(
            keyword in task.query.lower()
            for keyword in keywords
        )

    def execute(self, task):
        return f"{self.name} is researching the topic."


class DataAgent(Agent):
    def can_handle(self, task):
        keywords = ["data", "csv", "analysis", "dataset"]

        return any(
            keyword in task.query.lower()
            for keyword in keywords
        )

    def execute(self, task):
        return f"{self.name} is analyzing the data."


class AgentRouter:
    def __init__(self, agents):
        self.agents = agents

    def route(self, task):
        for agent in self.agents:
            if agent.can_handle(task):
                return agent.execute(task)

        return "No suitable agent found."


agents = [
    CodingAgent("CodeAgent"),
    ResearchAgent("ResearchAgent"),
    DataAgent("DataAgent")
]

router = AgentRouter(agents)

tasks = [
    Task("Fix this Python bug"),
    Task("Research the latest RAG techniques"),
    Task("Analyze this CSV dataset"),
    Task("Book me a hotel")
]

for task in tasks:
    print(task.query)
    print(router.route(task))
    print("-" * 40)