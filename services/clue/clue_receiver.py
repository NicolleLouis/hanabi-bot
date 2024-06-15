from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from models.card.physical_card import PhysicalCard
from models.clue import Clue

if TYPE_CHECKING:
    from models.game import Game
    from models.card.card import Card
    from models.player import Player


class ClueReceiverException(Exception):
    pass


class ClueReceiver:
    def __init__(self, game: Game):
        self.game = game

    def receive_clue(self, data: Optional[dict] = None, clue: Optional[Clue] = None) -> None:
        if clue is None:
            if data is None:
                raise ClueReceiverException("No clue or data provided")
            clue = Clue(data)
        focus = self.find_focus(clue)
        self.analyse_clue(clue, focus)
        self.save_clue_information(clue)

    def analyse_clue(self, clue: Clue, focus: Card) -> None:
        chop = self.get_player(clue).get_chop()
        if focus != chop:
            self.compute_possible_play_cards(focus, clue)
        if focus == chop:
            self.compute_possible_save_cards(focus, clue)

    def compute_possible_play_cards(self, card: Card, clue: Clue):
        if clue.is_color_clue:
            playable_rank = self.game.board.get_playable_rank(clue.value)
            if playable_rank is None:
                print("Did not understand this play clue")
                return
            card.set_known(suit=clue.value, rank=playable_rank)
        else:
            playable_suits = self.game.board.get_playable_suits(clue.value)
            print(playable_suits)
            if len(playable_suits) == 0:
                print("Did not understand this play clue")
                return
            if len(playable_suits) == 1:
                card.set_known(suit=playable_suits[0], rank=clue.value)
            else:
                possibilities = [PhysicalCard(suit=suit, rank=clue.value) for suit in playable_suits]
                card.set_among_possibilities(possibilities)
        card.computed_info.playable = True

    # ToDo add me
    def compute_possible_save_cards(self, card, clue):
        pass

    def get_player(self, clue) -> Player:
        return self.game.player_finder.get_player(clue.player_index)

    def touched_cards(self, clue: Clue) -> List[Card]:
        cards_touched = []
        for card in self.get_player(clue).hand:
            if card.order in clue.card_orders_touched:
                cards_touched.append(card)
        return cards_touched

    def find_focus(self, clue) -> Card:
        touched_cards = self.touched_cards(clue)
        # Case single card touched
        if len(touched_cards) == 1:
            return touched_cards[0]

        previously_unclued_cards = [card for card in touched_cards if not card.touched]

        # Case no new cards clued
        if len(previously_unclued_cards) == 0:
            return touched_cards[-1]

        # Case single new card clued
        if len(previously_unclued_cards) == 1:
            return previously_unclued_cards[0]

        # Case chop touched
        chop = self.get_player(clue).get_chop()
        if chop in touched_cards:
            return chop

        # Case multiple new cards clued and no chop
        return previously_unclued_cards[-1]

    def save_clue_information(self, clue: Clue) -> None:
        for card in self.get_player(clue).hand:
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
