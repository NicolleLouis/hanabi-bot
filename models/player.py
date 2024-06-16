from __future__ import annotations

from typing import List, TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from models.deck import Deck

from models.card.card import Card


class PlayerException(Exception):
    pass


class Player:
    def __init__(self, name, index):
        self.name = name
        self.index = index
        self.hand = []

    def __str__(self):
        return f"{self.name} ({self.index})"

    def pretty_print(self) -> None:
        print(f"Player: {self}")
        print("Hand:")
        for card in self.hand:
            card.pretty_print()

    # Cards are added oldest to newest, so "slot 1" is the final element in the list
    def get_card_by_slot(self, slot_number):
        return self.hand[-slot_number]

    @property
    def touched_cards(self) -> List[Card]:
        return [card for card in self.hand if card.touched]

    @property
    def unclued_cards(self) -> List[Card]:
        return [card for card in self.hand if not card.touched]

    @property
    def playable_cards(self):
        return [card for card in self.hand if card.playable]

    @property
    def trash_cards(self):
        return [card for card in self.hand if card.trash]

    def has_card(self, card):
        return len([c for c in self.hand if c.order == card.order]) > 0

    def get_finesse(self) -> Optional[Card]:
        if len(self.unclued_cards) == 0:
            return None
        return self.unclued_cards[-1]

    def get_chop(self) -> Optional[Card]:
        if len(self.unclued_cards) == 0:
            return None
        return self.unclued_cards[0]

    def remove_card_from_hand(self, card_order) -> Card:
        card = self.get_card(card_order)
        self.hand.remove(card)
        return card

    def get_card(self, card_order) -> Card:
        for card in self.hand:
            if card.order == card_order:
                return card
        raise PlayerException(f"Card {card_order} not found in hand")

    def add_card_to_hand(self, card_order, card_rank, card_suit, deck: Optional[Deck] = None) -> None:
        card = Card(
            order=card_order,
            rank=card_rank,
            suit=card_suit,
            deck=deck
        )
        self.hand.append(card)

    def has_card(self, card: Card):
        return len([c for c in self.hand if c.order == card.order]) > 0
