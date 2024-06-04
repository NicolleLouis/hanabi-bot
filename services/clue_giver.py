from __future__ import annotations

from typing import TYPE_CHECKING

from constants.actions import ACTION

if TYPE_CHECKING:
    from models.card import Card
    from models.player import Player


class ClueGiver:
    def __init__(self, player: Player, is_color_clue: bool):
        self.player = player
        self.is_color_clue = is_color_clue

    def build(self, card: Card) -> dict:
        body = {
            "target": self.player.index,
        }
        if self.is_color_clue:
            body["type"] = ACTION.COLOR_CLUE
            body["value"] = card.suit
        else:
            body["type"] = ACTION.RANK_CLUE
            body["value"] = card.rank
        return body

    def to_card(self, card: Card):
        return self.build(card)

    def to_slot(self, slot_number: int):
        return self.build(self.player.get_card_by_slot(slot_number))

    def to_chop(self):
        return self.build(self.player.get_chop())
