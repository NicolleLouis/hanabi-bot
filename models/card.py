from constants.color import Color


class Card:
    def __init__(self, color: str, value: int):
        if color not in Color.ALL_COLORS:
            raise ValueError("Invalid color")
        if value not in range(1, 6):
            raise ValueError("Invalid value")
        self.color = color
        self.value = value

    def __str__(self):
        return f"{self.color} {self.value}"
