from __future__ import annotations

import random
import uuid
from typing import Optional, Set, TYPE_CHECKING

if TYPE_CHECKING:   # pragma: no cover
    from models.card import Card


class CardPile:
    def __init__(self, cards: Optional[Set[Card]] = None):
        if cards is None:
            cards = set()
        self.cards = cards.copy()
        self.id = uuid.uuid4()

    def __hash__(self):
        return self.id.int

    def __eq__(self, other):
        return other.cards == self.cards

    def __len__(self):
        return len(self.cards)

    def __str__(self):
        return f"{len(self)} cards in pile"

    def __add__(self, other):
        return CardPile(self.cards | other.cards)

    def __sub__(self, other):
        return CardPile(self.cards - other.cards)

    def add_card(self, card: Card):
        self.cards.add(card)

    def pretty_print(self):
        for card in self.cards:
            print(card)

    # This pick cards from the pile but doesn't remove them
    def pick_cards(self, card_number):
        if card_number > len(self.cards):
            card_number = len(self.cards)
        return CardPile(set(random.sample(self.cards, card_number)))

    # This draw card from the pile, so it removes them
    def draw_cards(self, card_number):
        drawn_cards = self.pick_cards(card_number)
        self.cards -= drawn_cards.cards
        return drawn_cards

    def is_empty(self):
        return len(self) == 0

    def has_card_equivalent(self, card: Card):
        return any(card.equivalent(own_card) for own_card in self.cards)

    def number_of_cards_like(self, card: Card):
        return sum(card.equivalent(own_card) for own_card in self.cards)
