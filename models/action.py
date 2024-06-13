from typing import Optional

from constants.action_source import ActionSource


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
        return f"{self.source} -> {self.target} : {self.value} (Score: {self.score})"
