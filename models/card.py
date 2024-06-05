from models.computed_info import ComputedInfo
from models.known_info import KnownInfo


class Card:
    def __init__(
            self,
            order: int,
            suit: int,
            rank: int,
    ):
        self.order = order
        self.suit = suit
        self.rank = rank
        self.known_info = KnownInfo()
        self.computed_info = ComputedInfo()

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    def pretty_print(self) -> None:
        print("Card:")
        print(self)
        print(f"Order: {self.order}")
        self.known_info.pretty_print()
        self.computed_info.pretty_print()

    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit and self.order == other.order

    def equivalent(self, other):
        return self.rank == other.rank and self.suit == other.suit

    def touched(self):
        return self.known_info.touched or self.computed_info.touched
