from __future__ import annotations

from typing import Optional, List

from models.card.physical_card import PhysicalCard
from models.stack import Stack


class BoardException(Exception):
    pass


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
        stack = self.get_stack(card.suit)
        return stack.is_card_valid(card)

    def get_stack(self, suit: int) -> Stack:
        for stack in self.stacks:
            if stack.suit == suit:
                return stack
        raise BoardException(f"Stack with suit {suit} not found")

    def is_already_played(self, card: PhysicalCard):
        stack = self.get_stack(card.suit)
        return card in stack.played_cards

    def get_played_cards(self):
        played_cards = []
        for stack in self.stacks:
            played_cards.extend(stack.played_cards)
        return played_cards

    def get_playable_rank(self, suit: int) -> Optional[int]:
        stack = self.get_stack(suit)
        return stack.get_playable_rank()

    def get_playable_suits(self, rank: int) -> Optional[List[int]]:
        playable_suits = []
        for stack in self.stacks:
            if stack.is_card_valid(PhysicalCard(suit=stack.suit, rank=rank)):
                playable_suits.append(stack.suit)
        return playable_suits
