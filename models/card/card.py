from __future__ import annotations

from models.card.computed_info import ComputedInfo
from models.card.known_info import KnownInfo
from models.card.physical_card import PhysicalCard

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from models.deck import Deck


class Card:
    def __init__(
            self,
            order: int,
            suit: int,
            rank: int,
            deck: Optional[Deck] = None,
    ):
        self.order = order
        self.physical_card = PhysicalCard(
            suit=suit,
            rank=rank
        )
        self.known_info = KnownInfo(self)
        self.computed_info = ComputedInfo(deck=deck)

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    def pretty_print(self) -> None:
        print("Card:")
        print(self)
        print(f"Order: {self.order}")
        self.known_info.pretty_print()
        self.computed_info.pretty_print()

    @property
    def rank(self):
        return self.physical_card.rank

    @property
    def suit(self):
        return self.physical_card.suit

    def set_suit(self, suit):
        self.physical_card.suit = suit

    def set_rank(self, rank):
        self.physical_card.rank = rank

    def __eq__(self, other):
        return self.physical_card == other.physical_card and self.order == other.order

    def touched(self):
        return self.known_info.touched or self.computed_info.touched
