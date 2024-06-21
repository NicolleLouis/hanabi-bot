from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Union

from models.card.physical_card import PhysicalCard
from models.clue import Clue
from models.card.card import Card
from services.card import CardService

if TYPE_CHECKING:
    from models.game import Game
    from models.player import Player


class ClueReceiverException(Exception):
    pass


class ClueReceiver:
    def __init__(self, game: Game):
        self.game = game

    def receive_clue(self, clue: Clue) -> None:
        focus = self.find_focus(clue)
        self.analyse_clue(clue, focus)
        self.save_clue_information(clue)

    def clue_giver(self) -> Player:
        return self.game.player_finder.get_player(self.game.current_player_index)

    def clue_receiver(self, clue: Clue) -> Player:
        return self.game.player_finder.get_player(clue.player_index)

    def self_player(self) -> Player:
        return self.game.player_finder.find_self()

    def analyse_clue(self, clue: Clue, focus: Card) -> None:
        chop = self.get_player(clue).get_chop()
        if focus == chop:
            self.compute_possible_save_cards(focus, clue)
        else:
            self.compute_possible_play_cards(focus, clue)

    def compute_possible_play_cards(self, card: Card, clue: Clue):
        if clue.is_color_clue:
            self.compute_possible_play_color_clue(card, clue)
        else:
            if self.self_player() not in [self.clue_receiver(clue), self.clue_giver()]:
                self.compute_own_hand_consequences(card, clue)
            self.compute_possible_play_rank_clue(card, clue)

    # For now it's only play clues so the card is promised playable.
    # So we have to dig for the missing ones.
    def compute_own_hand_consequences(self, card: Card, clue: Clue):
        missing_cards = self.game.board.get_missing_card_before_play(card)

    def compute_possible_play_color_clue(self, card: Card, clue: Clue):
        playable_rank = self.game.board.get_playable_rank(clue.value)
        if playable_rank is None:
            print("Did not understand this play clue")
            print(f"Clue receiver: {self.clue_receiver(clue).name}")
            return
        card.set_known(suit=clue.value, rank=playable_rank)
        card.computed_info.playable = True

    def compute_possible_play_rank_clue(self, card: Card, clue: Clue):
        playable_suits = self.game.board.get_playable_suits(clue.value)
        if len(playable_suits) == 0:
            print("Did not understand this play clue")
            print(f"Clue receiver: {self.clue_receiver(clue).name}")
            return
        if len(playable_suits) == 1:
            card.set_known(suit=playable_suits[0], rank=clue.value)
        else:
            possibilities = [PhysicalCard(suit=suit, rank=clue.value) for suit in playable_suits]
            card.set_among_possibilities(possibilities)
        card.computed_info.playable = True

    def compute_possible_save_cards(self, card, clue):
        if self.is_legal_save_clue(clue):
            possible_save_cards = CardService.convert_to_physical_cards(
                self.get_possible_save_cards(clue)
            )
            if len(possible_save_cards) == 0:
                print("Did not understand this save clue")
                return
            if len(possible_save_cards) == 1:
                save_card = possible_save_cards[0]
                card.set_known(suit=save_card.suit, rank=save_card.rank)
            else:
                card.set_among_possibilities(possible_save_cards)
        else:
            # It was actually a play clue
            self.compute_possible_play_cards(card, clue)

    def get_possible_save_cards(self, clue: Clue) -> List[Union[Card, PhysicalCard]]:
        if clue.is_color_clue:
            save_cards = [card for card in self.game.board.discard_pile if card.physical_card.suit == clue.value]
            save_cards = [card for card in save_cards if card.physical_card.rank != 5]
            return save_cards
        else:
            if clue.value == 5:
                return [card for card in self.game.deck.cards if card.rank == 5]
            elif clue.value == 2:
                return [card for card in self.game.deck.cards if card.rank == 2]
            else:
                return [card for card in self.game.board.discard_pile if card.physical_card.rank == clue.value]

    def is_legal_save_color_clue(self, clue: Clue) -> bool:
        played_cards = self.game.board.get_played_cards()
        potential_saved_cards = [card for card in self.game.board.discard_pile if card.physical_card.suit == clue.value]
        # Remove 1s
        potential_saved_cards = [card for card in potential_saved_cards if card.physical_card.rank != 1]
        for card in potential_saved_cards:
            if card not in played_cards:
                return True
        return False

    def is_legal_save_rank_clue(self, clue: Clue) -> bool:
        played_cards = self.game.board.get_played_cards()
        if clue.value == 5:
            return True
        elif clue.value == 1:
            return False
        # Legal if at least one 2 is not played
        elif clue.value == 2:
            for stack in self.game.board.stacks:
                if stack.current_rank < 2:
                    return True
        else:
            # For 3 and 4, it's legal if there is at least one of them in discard and not played
            potential_saved_cards = [card for card in self.game.board.discard_pile if card.physical_card.rank == clue.value]
            for card in potential_saved_cards:
                if card not in played_cards:
                    return True
        return False

    def is_legal_save_clue(self, clue: Clue) -> bool:
        if clue.is_color_clue:
            return self.is_legal_save_color_clue(clue)
        else:
            return self.is_legal_save_rank_clue(clue)

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
