from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.game import Game


class PlayerFinderException(Exception):
    pass


class PlayerFinder:
    def __init__(self, game: Game):
        self.game = game

    def clean_index(self, player_index):
        return player_index % len(self.game.players)

    def find_self(self):
        return self.get_player(self.game.own_index)

    def get_player(self, player_index):
        try:
            return self.game.players[self.clean_index(player_index)]
        except IndexError:
            raise PlayerFinderException(f"Player with index {self.clean_index(player_index)} not found")

    def next_seated_player(self, from_seat=None, skip=0):
        if from_seat is None:
            from_seat = self.game.own_index
        return self.get_player(from_seat + skip + 1)

    def next_playing_player(self, skip=0):
        from_seat = self.game.current_player_index
        return self.get_player(from_seat + skip + 1)
