from typing import Optional, List

from constants.action_source import ActionSource
from constants.actions import ACTION
from models.action import Action


class ClueException(Exception):
    pass


class Clue:
    def __init__(
            self,
            data: Optional[dict] = None,
            player_index: Optional[int] = None,
            is_color_clue: Optional[bool] = None,
            value: Optional[int] = None,
            card_orders_touched: Optional[List[int]] = None,
            score: Optional[int] = None,
    ):
        self.check_legality(
            data=data,
            player_index=player_index,
            is_color_clue=is_color_clue,
            value=value,
            card_orders_touched=card_orders_touched
        )

        if data is not None:
            self.player_index = data["target"]
            self.is_color_clue = data["clue"]["type"] == 0
            self.value = data["clue"]["value"]
            self.card_orders_touched = data["list"]
            return

        if player_index is not None:
            self.player_index = player_index
        if is_color_clue is not None:
            self.is_color_clue = is_color_clue
        if value is not None:
            self.value = value
        if card_orders_touched is not None:
            self.card_orders_touched = card_orders_touched

        self.score = score

    def __str__(self):
        return f"Clue: To:{self.player_index} - is_color:{self.is_color_clue} - value:{self.value}"

    def __eq__(self, other):
        if self.player_index != other.player_index:
            return False
        if self.is_color_clue != other.is_color_clue:
            return False
        if self.value != other.value:
            return False
        if len([card for card in self.card_orders_touched if card not in other.card_orders_touched]) > 0:
            return False
        if len([card for card in other.card_orders_touched if card not in self.card_orders_touched]) > 0:
            return False
        return True

    @staticmethod
    def check_legality(
            data: Optional[dict] = None,
            player_index: Optional[int] = None,
            is_color_clue: Optional[bool] = None,
            value: Optional[int] = None,
            card_orders_touched: Optional[List[int]] = None
    ) -> None:
        if data is not None:
            return
        if player_index is None:
            raise ClueException("player_index is required")
        if is_color_clue is None:
            raise ClueException("is_color_clue is required")
        if value is None:
            raise ClueException("value is required")
        if card_orders_touched is None:
            raise ClueException("card_orders_touched is required")

    def to_action(self, source: Optional[ActionSource] = None) -> Action:
        if self.is_color_clue:
            action_type = ACTION.COLOR_CLUE
        else:
            action_type = ACTION.RANK_CLUE
        return Action(
            action_type=action_type,
            target=self.player_index,
            value=self.value,
            source=source,
            score=self.score,
        )
