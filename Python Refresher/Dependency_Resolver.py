class DependencyResolver:

    def __init__(self, dependencies):
        self.graph = dependencies
        self.visiting = set()
        self.visited = set()
        self.order = []

    def dfs(self, package):
        if package in self.visiting:
            raise ValueError(
                f"Circular dependency detected at: {package}"
            )

        if package in self.visited:
            return

        self.visiting.add(package)

        for dependency in self.graph.get(package, []):
            self.dfs(dependency)

        self.visiting.remove(package)
        self.visited.add(package)

        self.order.append(package)

    def resolve(self):
        for package in self.graph:
            self.dfs(package)

        return self.order[::-1]


dependencies = {
    "app": ["database", "api"],
    "api": ["auth"],
    "database": ["config"],
    "auth": ["config"],
    "config": []
}

resolver = DependencyResolver(dependencies)

print(resolver.resolve())