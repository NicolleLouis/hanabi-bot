from __future__ import annotations

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from models.game import Game
    from models.card import Card


class ClueReceiver:
    def __init__(self, game: Game):
        self.game = game

    def receive_clue(self, data):
        self.save_clue_information(data)

    def touched_cards(self, data) -> List[Card]:
        cards_touched = []
        player = self.game.player_finder.get_player(data["player"])
        for card in player.hand:
            if card.order in data["list"]:
                cards_touched.append(card)
        return cards_touched

    def find_focus(self, data) -> Card:
        touched_cards = self.touched_cards(data)
        if len(touched_cards) == 1:
            return touched_cards[0]
        raise NotImplementedError("Focus not implemented for multiple cards")

    def save_clue_information(self, data) -> None:
        player = self.game.player_finder.get_player(data["target"])
        is_color_clue = data["clue"]["type"] == 1
        value = data["clue"]["value"]
        cards_touched = data["list"]
        for card in player.hand:
            if card.order in cards_touched:
                card.known_info.add_positive_clue(is_color_clue, value)
            else:
                card.known_info.add_negative_clue(is_color_clue, value)
