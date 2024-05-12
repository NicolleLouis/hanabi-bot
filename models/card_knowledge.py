from constants.color import Color
from exceptions.models.card_knowledge import CardKnowledgeException


class CardKnowledge:
    def __init__(self):
        self.possible_colors = Color.ALL_COLORS.copy()
        self.possible_values = list(range(1, 6))

        self.is_known = False

        self.known_color = None
        self.known_value = None

    def __str__(self):
        if self.is_known:
            return f'Known: {self.known_color} {self.known_value}'
        return f'Unknown: {len(self.possible_colors)} colors possible and {len(self.possible_values)} potential values'

    def add_positive_color_information(self, color: str) -> None:
        if color not in self.possible_colors:
            raise CardKnowledgeException(self, 'Incoherent color information')

        self.possible_colors = [color]
        self.clean()

    def add_positive_value_information(self, value: int) -> None:
        if value not in self.possible_values:
            raise CardKnowledgeException(self, 'Incoherent value information')

        self.possible_values = [value]
        self.clean()

    def add_negative_color_information(self, color: str) -> None:
        self.possible_colors.remove(color)
        self.clean()

    def add_negative_value_information(self, value: int) -> None:
        self.possible_values.remove(value)
        self.clean()

    def clean(self) -> None:
        self.sanity_check()

        if len(self.possible_colors) == 1:
            self.known_color = self.possible_colors[0]

        if len(self.possible_values) == 1:
            self.known_value = self.possible_values[0]

        if self.known_value is not None and self.known_color is not None:
            self.is_known = True

    def sanity_check(self) -> None:
        if len(self.possible_values) == 0:
            raise CardKnowledgeException(self, "No possible values")

        if len(self.possible_colors) == 0:
            raise CardKnowledgeException(self, "No possible colors")
