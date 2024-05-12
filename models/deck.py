from constants.color import Color
from models.card import Card
from models.card_pile import CardPile


class Deck:
    def __init__(self):
        self.cards = CardPile()
        self.populate()

    def populate(self):
        for color in Color.ALL_COLORS:
            self.populate_color(color)

    def populate_color(self, color: str):
        repartition = {
            1: 3,
            2: 2,
            3: 2,
            4: 2,
            5: 1,
        }
        for value, number in repartition.items():
            for _ in range(number):
                self.cards.add_card(Card(color, value))
