from __future__ import annotations

from typing import TYPE_CHECKING, Optional, List

from services.clue.clue_finder import ClueFinder
from services.clue.clue_receiver import ClueReceiver
from services.discard import DiscardService
from services.play import PlayService

if TYPE_CHECKING:
    from models.card.physical_card import PhysicalCard
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
            return self.play_service.to_card(self.player.playable_cards[0])

        if self.game.clue_tokens == 0:
            return self.discard()

        play_clues = self.clue_finder.find_play_clues()
        if len(play_clues) > 0:
            ordered_play_clues = sorted(play_clues, key=self.clue_finder.clue_score, reverse=True)
            return ordered_play_clues[0].to_action()
        else:
            return self.discard()

    def discard(self):
        trash_cards = self.player.trash_cards
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
        return len(self.player.playable_cards) > 0

    def display_card_options(self):
        print("Card Options:")
        for card in self.player.hand:
            print(card)
            card.computed_info.pretty_print()

    # Beware touched cards by ourselves (Might be duplicated)
    def get_known_cards(self) -> List[PhysicalCard]:
        played_cards = self.game.board.get_played_cards()
        touched_cards = []
        for player in self.game.players:
            touched_cards.extend([card.physical_card for card in player.touched_cards])
        return played_cards + touched_cards

    def good_touch_elimination(self):
        played_cards = self.get_known_cards()
        for card in self.player.touched_cards:
            for played_card in played_cards:
                card.computed_info.remove_possibility(played_card)

    def update_playability(self):
        for card in self.player.hand:
            card.computed_info.update_playability(self.game.board)

    def receive_clue(self, data):
        self.clue_receiver.receive_clue(data=data)
        self.good_touch_elimination()
        self.update_playability()
