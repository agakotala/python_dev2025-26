class Rectangle:
    def __init__(self, width: float, height: float) -> None:
        if width <= 0 or height <= 0:
            raise ValueError("Szerokość i wysokość muszą być > 0.")
        self.width = float(width)
        self.height = float(height)

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)
r = Rectangle(3, 4)

print(r.area())
print(r.perimeter())  