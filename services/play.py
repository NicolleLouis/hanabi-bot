from __future__ import annotations

from typing import TYPE_CHECKING

from constants.actions import ACTION
from models.action import Action

if TYPE_CHECKING:
    from models.card import Card
    from models.player import Player


class PlayService:
    def __init__(self, player: Player):
        self.player = player

    @staticmethod
    def build(card: Card) -> Action:
        return Action(action_type=ACTION.PLAY, target=card.order)

    def to_card(self, card: Card):
        return self.build(card)

    def to_slot(self, slot_number: int):
        return self.build(self.player.get_card_by_slot(slot_number))

    def to_chop(self):
        return self.build(self.player.get_chop())

    def to_finesse(self):
        return self.build(self.player.get_finesse())
