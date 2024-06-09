from __future__ import annotations

from models.card.physical_card import PhysicalCard


class StackException(Exception):
    pass


class Stack:
    def __init__(self, suit):
        self.suit = suit
        self.current_rank = 0

    def __str__(self):
        return f"Stack {self.suit}: {self.current_rank}"

    def add_card(self, card: PhysicalCard):
        try:
            self.check_card_validity(card)
        except StackException:
            return False

        self.current_rank += 1
        return True

    def check_card_validity(self, card: PhysicalCard):
        if card.suit != self.suit:
            raise StackException("Card suit does not match stack suit")

        if card.rank != self.current_rank + 1:
            raise StackException("Card rank is not the next in the stack")

    def is_card_valid(self, card: PhysicalCard):
        try:
            self.check_card_validity(card)
        except StackException:
            return False
        return True

    @property
    def played_cards(self):
        return [PhysicalCard(suit=self.suit, rank=rank) for rank in range(1, self.current_rank+1)]
