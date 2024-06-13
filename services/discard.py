from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from constants.action_source import ActionSource
from constants.actions import ACTION
from models.action import Action

if TYPE_CHECKING:
    from models.card.card import Card
    from models.player import Player


class DiscardService:
    def __init__(self, player: Player):
        self.player = player

    @staticmethod
    def build(card: Card, score: Optional[int] = None) -> Action:
        return Action(
            action_type=ACTION.DISCARD,
            target=card.order,
            source=ActionSource.DISCARD,
            score=score,
        )

    def to_card(self, card: Card, score: Optional[int] = None):
        return self.build(card, score)

    def to_slot(self, slot_number: int, score: Optional[int] = None):
        return self.build(self.player.get_card_by_slot(slot_number), score)

    def to_chop(self, score: Optional[int] = None):
        return self.build(self.player.get_chop(), score)
