from __future__ import annotations

from typing import TYPE_CHECKING

from services.discard import DiscardService
from services.clue_giver import ClueGiver

if TYPE_CHECKING:
    from models.game import Game


class Brain:
    def __init__(self, game: Game):
        self.game = game
        self.player = None
        self.discard_service = None

    def set_player(self, player):
        self.player = player
        self.discard_service = DiscardService(player)

    def player_finder(self):
        return self.game.player_finder

    def find_action(self):
        if self.game.clue_tokens > 0:
            return ClueGiver(self.player_finder().next_seated_player(), is_color_clue=True).to_slot(1)
        else:
            return self.discard_service.to_chop()
