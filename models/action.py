from typing import Optional

from constants.action_source import ActionSource
from constants.actions import ACTION
from services.action import ActionService
from services.color_service import ColorService


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
