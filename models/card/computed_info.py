from __future__ import annotations

from typing import TYPE_CHECKING, Optional


if TYPE_CHECKING:
    from models.board import Board
    from models.card.physical_card import PhysicalCard
    from models.card.known_info import KnownInfo
    from models.deck import Deck


class ComputedInfo:
    def __init__(self, deck: Optional[Deck] = None):
        self.touched = False
        self.trash = False
        self.playable = False
        self.possible_cards: set = set()

        self.initialize_possible_cards(deck)

    def pretty_print(self) -> None:
        print("Computed Info:")
        print(f"Playable: {self.playable}")
        print(f"Number of possibilities: {len(self.possible_cards)}")
        if len(self.possible_cards) <= 5:
            self.display_possibilities()

    def display_possibilities(self):
        print(f"Possible Cards: {' '.join(map(str, self.possible_cards))}")

    def initialize_possible_cards(self, deck: Optional[Deck] = None):
        if deck is not None:
            self.possible_cards = set(deck.cards)

    def remove_possibility(self, physical_card: PhysicalCard):
        self.possible_cards.discard(physical_card)

    def update_from_known_info(self, known_info: KnownInfo):
        self.update_from_negative_rank_clues(known_info)
        self.update_from_negative_suit_clues(known_info)
        self.update_from_positive_rank_clues(known_info)
        self.update_from_positive_suit_clues(known_info)

    def update_from_negative_rank_clues(self, known_info: KnownInfo):
        for negative_rank in known_info.negative_rank_clues:
            self.possible_cards = {card for card in self.possible_cards if card.rank != negative_rank}

    def update_from_positive_rank_clues(self, known_info: KnownInfo):
        for positive_rank in known_info.positive_rank_clues:
            self.possible_cards = {card for card in self.possible_cards if card.rank == positive_rank}

    def update_from_negative_suit_clues(self, known_info: KnownInfo):
        for negative_suit in known_info.negative_suit_clues:
            self.possible_cards = {card for card in self.possible_cards if card.suit != negative_suit}

    def update_from_positive_suit_clues(self, known_info: KnownInfo):
        for positive_suit in known_info.positive_suit_clues:
            self.possible_cards = {card for card in self.possible_cards if card.suit == positive_suit}

    def set_trash(self):
        self.trash = True
        self.playable = False

    def update_playability(self, board: Board):
        if self.trash:
            return
        if len(self.possible_cards) == 0:
            self.set_trash()
            return

        if self.playable:
            return
        self.playable = all(board.is_card_valid(card) for card in self.possible_cards)
