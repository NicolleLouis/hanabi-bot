from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.card.card import Card
    from models.player import Player

from models.clue import Clue


class ClueBuilder:
    @staticmethod
    def generate_clue(player: Player, is_color_clue: bool, card: Card) -> Clue:
        if is_color_clue:
            value = card.suit
            cards_touched = [card for card in player.hand if card.suit == value]
        else:
            value = card.rank
            cards_touched = [card for card in player.hand if card.rank == value]
        return Clue(
            player_index=player.index,
            is_color_clue=is_color_clue,
            value=value,
            card_orders_touched=[card.order for card in cards_touched]
        )
