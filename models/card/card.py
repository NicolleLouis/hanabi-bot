from __future__ import annotations

from models.card.computed_info import ComputedInfo
from models.card.known_info import KnownInfo
from models.card.physical_card import PhysicalCard

from typing import TYPE_CHECKING, Optional, List, Union

from services.color_service import ColorService

if TYPE_CHECKING:
    from models.board import Board
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
        self.is_known = False
        self.known_info = KnownInfo(self)
        self.computed_info = ComputedInfo(deck=deck)

    def __str__(self):
        color = ColorService.translate_suit(self.suit)
        result = f"{color}{self.rank}"
        if self.is_known:
            result = f"Known Card: {result}"
        if self.touched:
            result += " (Touched)"
        return result

    def pretty_print(self) -> None:
        if self.is_known:
            print(f"Known Card: {self.rank} of {self.suit}")
            return

        print("Unknown Card: ")
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

    @property
    def touched(self):
        return self.known_info.touched or self.computed_info.touched

    @property
    def playable(self):
        return self.computed_info.playable

    def set_playable(self, playable: bool) -> None:
        self.computed_info.playable = playable

    def set_trash(self, trash: bool) -> None:
        self.computed_info.trash = trash

    @property
    def trash(self):
        return self.computed_info.trash

    def compute_is_known(self):
        if self.rank == -1 or self.suit == -1:
            self.is_known = False
        else:
            self.is_known = True

    def set_known(self, suit: int, rank: int):
        self.is_known = True
        self.set_rank(rank)
        self.set_suit(suit)

    def update_playability(self, board: Board):
        self.compute_is_known()
        if self.is_known:
            if board.is_card_valid(self.physical_card):
                self.set_playable(True)
                self.set_trash(False)
            else:
                self.set_playable(False)
                if board.is_already_played(self.physical_card):
                    self.set_trash(True)
            return
        self.computed_info.update_playability(board)

    def set_among_possibilities(self, possibilities: List[PhysicalCard]):
        self.computed_info.set_among_possibilities(set(possibilities))
