class Animal:
    """Base class representing a generic animal."""

    def __init__(self, name, sound):
        self.name = name
        self.sound = sound

    def speak(self):
        return f"{self.name} says {self.sound}"

    def __str__(self):
        return f"Animal({self.name})"


class Dog(Animal):
    """Dog subclass, inherits from Animal."""

    def __init__(self, name, breed):
        super().__init__(name, sound="Woof")
        self.breed = breed

    def fetch(self):
        return f"{self.name} fetches the ball!"


class Cat(Animal):
    """Cat subclass, inherits from Animal."""

    def __init__(self, name):
        super().__init__(name, sound="Meow")

    def scratch(self):
        return f"{self.name} scratches the post!"


def demo_polymorphism(animals):
    """Loop through different animal types and call shared method."""
    for animal in animals:
        print(animal.speak())


if __name__ == "__main__":
    fido = Dog("Fido", breed="Labrador")
    whiskers = Cat("Whiskers")

    print(fido)
    print(fido.speak())
    print(fido.fetch())

    print(whiskers.speak())
    print(whiskers.scratch())

    print("\nPolymorphism demo:")
    demo_polymorphism([fido, whiskers])

    print("\nClasses & OOP refresher complete.")