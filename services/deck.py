from __future__ import annotations

from collections import Counter
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from models.card.physical_card import PhysicalCard
    from models.deck import Deck


class DeckService:
    def __init__(self, deck: Deck):
        self.deck = deck

    def remaining_cards(self, discarded_cards: List[PhysicalCard]):
        counter_deck = Counter(self.deck.cards)
        counter_discarded = Counter(discarded_cards)
        counter_remaining = counter_deck - counter_discarded
        return list(counter_remaining.elements())

    def is_card_critical(self, card: PhysicalCard, discarded_cards: List[PhysicalCard]):
        remaining_cards = self.remaining_cards(discarded_cards)
        remaining_counter = Counter(remaining_cards)
        return remaining_counter[card] <= 1
