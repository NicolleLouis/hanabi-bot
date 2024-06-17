from __future__ import annotations

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from models.game import Game


from constants.action_source import ActionSource
from constants.actions import ACTION
from services.action import ActionService
from services.color_service import ColorService


class ActionException(Exception):
    pass


class Action:
    def __init__(
            self,
            action_type: str,
            target: int,
            value: Optional[int] = None,
            source: Optional[ActionSource] = None,
            score: Optional[int] = None,
    ):
        self.action_type = action_type
        self.target = target
        self.value = value
        self.source = source
        self.score = score

    def __str__(self):
        if self.action_type == ACTION.COLOR_CLUE:
            return self.string_case_color_clue()
        return f"{self.str_action_type()} ({str(self.source)}) -> {self.target} : {self.value} (Score: {self.score})"

    def str_action_type(self):
        return ActionService.translate_action(self.action_type)

    def string_case_color_clue(self):
        value = ColorService.translate_suit(self.value)
        return f"{self.str_action_type()} ({str(self.source)}) -> {self.target} : {value} (Score: {self.score})"

    def to_clue(self, game: Game):
        from models.clue import Clue

        if self.action_type not in [ACTION.COLOR_CLUE, ACTION.RANK_CLUE]:
            raise ActionException("This action is not a clue")

        player_targeted = game.player_finder.get_player(self.target)
        is_color_clue = self.action_type == ACTION.COLOR_CLUE
        if is_color_clue:
            card_orders_touched = [card.order for card in player_targeted.hand if card.suit == self.value]
        else:
            card_orders_touched = [card.order for card in player_targeted.hand if card.rank == self.value]

        return Clue(
            player_index=player_targeted.index,
            value=self.value,
            is_color_clue=is_color_clue,
            card_orders_touched=card_orders_touched
        )
