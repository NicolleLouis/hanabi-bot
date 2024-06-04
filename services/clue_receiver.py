from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.game import Game


class ClueReceiver:
    def __init__(self, game: Game):
        self.game = game

    def receive_clue(self, data):
        self.save_clue_information(data)

    def save_clue_information(self, data):
        player = self.game.player_finder.get_player(data["target"])
        is_color_clue = data["clue"]["type"] == 1
        value = data["clue"]["value"]
        cards_touched = data["list"]
        for card in player.hand:
            if card.order in cards_touched:
                card.known_info.add_positive_clue(is_color_clue, value)
            else:
                card.known_info.add_negative_clue(is_color_clue, value)
