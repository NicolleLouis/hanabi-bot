from __future__ import annotations

from typing import TYPE_CHECKING

from constants.actions import ACTION
from models.action import Action

if TYPE_CHECKING:
    from models.card import Card
    from models.player import Player


class ClueGiver:
    def __init__(self, player: Player, is_color_clue: bool):
        self.player = player
        self.is_color_clue = is_color_clue

    def build(self, card: Card) -> Action:
        target = self.player.index
        if self.is_color_clue:
            action_type = ACTION.COLOR_CLUE
            value = card.suit
        else:
            action_type = ACTION.RANK_CLUE
            value = card.rank

        return Action(action_type=action_type, target=target, value=value)

    def to_card(self, card: Card):
        return self.build(card)

    def to_slot(self, slot_number: int):
        return self.build(self.player.get_card_by_slot(slot_number))

    def to_chop(self):
        return self.build(self.player.get_chop())
