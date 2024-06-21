from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from models.card.physical_card import PhysicalCard
    from models.card.card import Card


class KnownInfoException(Exception):
    pass


class KnownInfo:
    def __init__(self, card: Card):
        self.card = card

        self.positive_rank_clues = []
        self.negative_rank_clues = []
        self.positive_suit_clues = []
        self.negative_suit_clues = []
        self.touched = False

    def pretty_print(self) -> None:
        print("Known Info:")
        print(f"Positive Rank Clues: {self.positive_rank_clues}")
        print(f"Negative Rank Clues: {self.negative_rank_clues}")
        print(f"Positive Suit Clues: {self.positive_suit_clues}")
        print(f"Negative Suit Clues: {self.negative_suit_clues}")
        print(f"Touched: {self.touched}")

    def add_positive_clue(self, is_color_clue: bool, value: int) -> None:
        if is_color_clue:
            self.positive_suit_clues.append(value)
        else:
            self.positive_rank_clues.append(value)
        self.touched = True

        self.update_computed_infos()
        self.check_sanity()

    def add_negative_clue(self, is_color_clue: bool, value: int) -> None:
        if is_color_clue:
            self.negative_suit_clues.append(value)
        else:
            self.negative_rank_clues.append(value)

        self.update_computed_infos()
        self.check_sanity()

    def check_sanity(self) -> bool:
        if self.touched:
            if len(self.positive_rank_clues) + len(self.positive_suit_clues) == 0:
                raise KnownInfoException("KnownInfo is touched but has no positive clues")

        for rank in self.negative_rank_clues:
            if rank in self.positive_rank_clues:
                raise KnownInfoException(f"Rank {rank} is both positive and negative")

        for suit in self.negative_suit_clues:
            if suit in self.positive_suit_clues:
                raise KnownInfoException(f"Suit {suit} is both positive and negative")

        return True

    def update_computed_infos(self):
        self.card.computed_info.update_from_known_info(self)

    def match_positive_clue(self, physical_card: PhysicalCard):
        if physical_card.rank in self.positive_rank_clues:
            return True
        if physical_card.suit in self.positive_suit_clues:
            return True
        return False
