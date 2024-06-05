from __future__ import annotations

from typing import TYPE_CHECKING, List

from models.clue import Clue

if TYPE_CHECKING:
    from models.game import Game
    from models.card import Card


class ClueReceiver:
    def __init__(self, game: Game):
        self.game = game

    def receive_clue(self, data):
        clue = Clue(data)
        self.save_clue_information(clue)

    def touched_cards(self, clue: Clue) -> List[Card]:
        cards_touched = []
        player = self.game.player_finder.get_player(clue.player_index)
        for card in player.hand:
            if card.order in clue.card_orders_touched:
                cards_touched.append(card)
        return cards_touched

    def find_focus(self, clue) -> Card:
        touched_cards = self.touched_cards(clue)
        if len(touched_cards) == 1:
            return touched_cards[0]
        raise NotImplementedError("Focus not implemented for multiple cards")

    def save_clue_information(self, clue: Clue) -> None:
        player = self.game.player_finder.get_player(clue.player_index)
        for card in player.hand:
            if card.order in clue.card_orders_touched:
                card.known_info.add_positive_clue(
                    clue.is_color_clue,
                    clue.value
                )
            else:
                card.known_info.add_negative_clue(
                    clue.is_color_clue,
                    clue.value
                )
