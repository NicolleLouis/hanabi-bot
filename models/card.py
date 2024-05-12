import uuid

from constants.color import Color


class Card:
    def __init__(self, color: str, value: int):
        if color not in Color.ALL_COLORS:
            raise ValueError("Invalid color")
        if value not in range(1, 6):
            raise ValueError("Invalid value")
        self.color = color
        self.value = value

        self.id = uuid.uuid4()

    def __hash__(self):
        return self.id.int

    def __str__(self):
        return f"{self.color} {self.value}"

    def equivalent(self, other):
        return self.color == other.color and self.value == other.value
