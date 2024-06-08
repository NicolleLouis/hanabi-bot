from __future__ import annotations

from typing import TYPE_CHECKING

from services.clue_receiver import ClueReceiver
from services.discard import DiscardService
from services.clue_giver import ClueGiver
from services.play import PlayService

if TYPE_CHECKING:
    from models.game import Game
    from models.player import Player


class Brain:
    def __init__(self, game: Game):
        self.game = game
        self.player = None
        self.discard_service = None
        self.play_service = None
        self.clue_receiver = ClueReceiver(game)

    def set_player(self, player: Player):
        self.player = player
        self.discard_service = DiscardService(player)
        self.play_service = PlayService(player)

    @property
    def player_finder(self):
        return self.game.player_finder

    def has_playable_cards(self):
        return len(self.player.playable_cards()) > 0

    def find_action(self):
        if self.has_playable_cards():
            return self.play_service.to_card(self.player.playable_cards()[0])
        if self.game.clue_tokens > 0:
            return ClueGiver(self.player_finder.next_seated_player(), is_color_clue=True).to_slot(1)
        else:
            return self.discard_service.to_chop()

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
        print(self.game.board)
        for card in self.player.hand:
            card.computed_info.update_playability(self.game.board)

    def receive_clue(self, data):
        self.clue_receiver.receive_clue(data=data)
        self.good_touch_elimination()
        self.update_playability()
