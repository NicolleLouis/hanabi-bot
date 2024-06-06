from typing import Optional


class Action:
    def __init__(
            self,
            action_type: str,
            target: int,
            value: Optional[int] = None,
    ):
        self.action_type = action_type
        self.target = target
        self.value = value

    def __str__(self):
        return f"{self.action_type} -> {self.target} : {self.value}"
