from abc import ABC, abstractmethod


class AIAgent(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def execute(self, task):
        pass


class ResearchAgent(AIAgent):
    def execute(self, task): # type: ignore
        return f"{self.name} is researching: {task}"


class CodingAgent(AIAgent):
    def execute(self, task): # type: ignore
        return f"{self.name} is generating code for: {task}"


class SummaryAgent(AIAgent):
    def execute(self, task): # type: ignore
        return f"{self.name} is summarizing: {task}"


class AgentManager:
    def __init__(self):
        self.agents = {}

    def register_agent(self, agent):
        self.agents[agent.name] = agent

    def run_task(self, agent_name, task):
        agent = self.agents.get(agent_name)

        if agent is None:
            return f"Agent '{agent_name}' not found!"

        return agent.execute(task)


# Usage
manager = AgentManager()

manager.register_agent(ResearchAgent("ResearchBot"))
manager.register_agent(CodingAgent("CodeBot"))
manager.register_agent(SummaryAgent("SummaryBot"))

print(manager.run_task("ResearchBot", "Latest RAG techniques"))
print(manager.run_task("CodeBot", "Build a FastAPI endpoint"))
print(manager.run_task("SummaryBot", "Summarize a research paper"))