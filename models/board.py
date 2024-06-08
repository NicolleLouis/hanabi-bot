from __future__ import annotations

from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from models.card.physical_card import PhysicalCard

from models.stack import Stack


class Board:
    def __init__(self, suits: Optional[List[int]] = None):
        self.stacks: List[Stack] = []
        for suit in suits:
            self.stacks.append(Stack(suit))

    def __str__(self):
        return f"Board: {' '.join(map(str, self.stacks))}"

    def add_card(self, card: PhysicalCard):
        for stack in self.stacks:
            if stack.add_card(card):
                return True
        return False

    def is_card_valid(self, card: PhysicalCard):
        for stack in self.stacks:
            if stack.is_card_valid(card):
                return True
        return False

    def get_played_cards(self):
        played_cards = []
        for stack in self.stacks:
            played_cards.extend(stack.played_cards)
        return played_cards