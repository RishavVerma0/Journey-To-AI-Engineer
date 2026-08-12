from collections import defaultdict


def build_order(tasks, dependencies):

    graph = defaultdict(list)

    for task, dependency in dependencies:
        graph[dependency].append(task)

    state = {}
    result = []

    def dfs(task):

        # Currently visiting → cycle detected
        if state.get(task) == 1:
            raise ValueError("Circular dependency detected")

        # Already completely processed
        if state.get(task) == 2:
            return

        state[task] = 1

        for next_task in graph[task]:
            dfs(next_task)

        state[task] = 2
        result.append(task)

    for task in tasks:
        if task not in state:
            dfs(task)

    return result[::-1]


tasks = [
    "Database",
    "Backend",
    "API",
    "Frontend"
]

dependencies = [
    ("Backend", "Database"),
    ("API", "Backend"),
    ("Frontend", "API")
]

print(build_order(tasks, dependencies))