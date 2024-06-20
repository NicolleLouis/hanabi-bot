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
            self.player_index = self.get_player_index(data)
            self.is_color_clue = self.get_is_color_clue(data)
            self.value = self.get_value(data)
            self.card_orders_touched = self.get_card_orders_touched(data)
            return

        self.player_index = player_index
        self.is_color_clue = is_color_clue
        self.value = value
        self.card_orders_touched = card_orders_touched

        self.score = score

    @staticmethod
    def get_card_orders_touched(data):
        if "list" in data:
            return data["list"]
        return data["card_orders_touched"]

    @staticmethod
    def get_player_index(data):
        if "target" in data:
            return data["target"]
        return data["player_index"]

    @staticmethod
    def get_value(data):
        if "clue" in data:
            return data["clue"]["value"]
        return data["value"]

    @staticmethod
    def get_is_color_clue(data):
        if "clue" in data:
            return data["clue"]["type"] == 0
        return data["is_color_clue"]

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
