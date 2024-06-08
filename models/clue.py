from typing import Optional, List


class ClueException(Exception):
    pass


class Clue:
    def __init__(
            self,
            data: Optional[dict] = None,
            player_index: Optional[int] = None,
            is_color_clue: Optional[bool] = None,
            value: Optional[int] = None,
            card_orders_touched: Optional[List[int]] = None
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

    def __str__(self):
        return f"Clue: To:{self.player_index} - is_color:{self.is_color_clue} - value:{self.value}"

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
