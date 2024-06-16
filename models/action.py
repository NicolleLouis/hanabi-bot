from typing import Optional

from constants.action_source import ActionSource
from services.action import ActionService


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
        action_type = ActionService.translate_action(self.action_type)
        return f"{action_type} ({self.source}) -> {self.target} : {self.value} (Score: {self.score})"
