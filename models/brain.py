from __future__ import annotations

import random
from typing import TYPE_CHECKING, Optional

from services.clue.clue_finder import ClueFinder
from services.clue.clue_receiver import ClueReceiver
from services.discard import DiscardService
from services.play import PlayService

if TYPE_CHECKING:
    from models.game import Game
    from models.player import Player


class Brain:
    def __init__(self, game: Game):
        self.game = game
        self.player = None
        self.discard_service: Optional[DiscardService] = None
        self.play_service: Optional[PlayService] = None
        self.clue_receiver: ClueReceiver = ClueReceiver(game)
        self.clue_finder: Optional[ClueFinder] = None

    # Main Action loop
    def find_action(self):
        if self.has_playable_cards():
            return self.play_service.to_card(self.player.playable_cards()[0])
        play_clues = self.clue_finder.find_play_clues()
        if len(play_clues) > 0:
            return random.choice(play_clues).to_action()
        else:
            return self.discard()

    def discard(self):
        trash_cards = self.player.trash_cards()
        if len(trash_cards) > 0:
            return self.discard_service.to_card(trash_cards[-1])
        return self.discard_service.to_chop()

    def set_player(self, player: Player):
        self.player = player
        self.discard_service = DiscardService(player)
        self.play_service = PlayService(player)
        self.clue_finder = ClueFinder(player, self.game)

    @property
    def player_finder(self):
        return self.game.player_finder

    def has_playable_cards(self):
        return len(self.player.playable_cards()) > 0

    def display_card_options(self):
        print("Card Options:")
        for card in self.player.hand:
            print(card)
            card.computed_info.pretty_print()

    # ToDo: for the moment only remove card already played and not cards touched in other player hands
    def good_touch_elimination(self):
        played_cards = self.game.board.get_played_cards()
        for card in self.player.hand:
            for played_card in played_cards:
                card.computed_info.remove_possibility(played_card)

    def update_playability(self):
        for card in self.player.hand:
            card.computed_info.update_playability(self.game.board)

    def receive_clue(self, data):
        self.clue_receiver.receive_clue(data=data)
        self.good_touch_elimination()
        self.update_playability()
