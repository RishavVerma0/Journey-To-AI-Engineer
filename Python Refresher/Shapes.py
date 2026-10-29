"""Program 2: Shapes
Demonstrates: abstract base classes, polymorphism, special methods.
"""

import math
from abc import ABC, abstractmethod


class Shape(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def area(self):
        """Every shape must be able to compute its area."""

    @abstractmethod
    def perimeter(self):
        """Every shape must be able to compute its perimeter."""

    def describe(self):
        return (f"{self.name}: area = {self.area():.2f}, "
                f"perimeter = {self.perimeter():.2f}")

    def __lt__(self, other):
        # Lets us sort shapes by area.
        return self.area() < other.area()


class Circle(Shape):
    def __init__(self, radius):
        super().__init__("Circle")
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2

    def perimeter(self):
        return 2 * math.pi * self.radius


class Rectangle(Shape):
    def __init__(self, width, height):
        super().__init__("Rectangle")
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)


class Square(Rectangle):
    def __init__(self, side):
        super().__init__(side, side)
        self.name = "Square"


if __name__ == "__main__":
    shapes = [Circle(3), Rectangle(4, 6), Square(5)]

    print("Shapes sorted by area:\n")
    for shape in sorted(shapes):
        print(shape.describe())  # same call, different behaviour per class

    try:
        Shape("Generic") # type: ignore
    except TypeError as e:
        print(f"\nCan't instantiate an abstract class: {e}")