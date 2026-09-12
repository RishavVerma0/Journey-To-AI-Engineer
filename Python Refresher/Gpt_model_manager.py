from abc import ABC, abstractmethod


class AIModel(ABC):
    def __init__(self, name, cost_per_token):
        self.name = name
        self.cost_per_token = cost_per_token

    @abstractmethod
    def generate(self, prompt):
        pass

    def calculate_cost(self, tokens):
        return tokens * self.cost_per_token


class FastModel(AIModel):
    def generate(self, prompt): # type: ignore
        return f"{self.name}: Fast response for '{prompt}'"


class ReasoningModel(AIModel):
    def generate(self, prompt): # type: ignore
        return f"{self.name}: Deep reasoning for '{prompt}'"


class LocalModel(AIModel):
    def generate(self, prompt): # type: ignore
        return f"{self.name}: Running locally for '{prompt}'"


class ModelManager:
    def __init__(self):
        self.models = {}

    def register(self, model):
        self.models[model.name] = model

    def run(self, model_name, prompt, tokens):
        if model_name not in self.models:
            print("Model not found")
            return

        model = self.models[model_name]

        response = model.generate(prompt)
        cost = model.calculate_cost(tokens)

        print(response)
        print(f"Estimated cost: ${cost:.6f}")


manager = ModelManager()

manager.register(
    FastModel("FastModel", 0.00001)
)

manager.register(
    ReasoningModel("ReasoningModel", 0.00003)
)

manager.register(
    LocalModel("LocalModel", 0)
)


manager.run(
    "FastModel",
    "Explain RAG",
    500
)

print()

manager.run(
    "ReasoningModel",
    "Design an AI agent",
    1200
)

print()

manager.run(
    "LocalModel",
    "Summarize this document",
    1000
)