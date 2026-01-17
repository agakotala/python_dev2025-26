class Dog:


    def __init__(self, name: str, age: int) -> None:
        if not name:
            raise ValueError("Imię nie może być puste.")
        if age < 0:
            raise ValueError("Wiek nie może być ujemny.")
        self.name = name
        self.age = age

    def bark(self) -> str:

        return "Hau!"

    def info(self) -> str:

        return f"{self.name} ({self.age})"

d = Dog("Reksio", 3)
print(d.bark())
print(d.info())