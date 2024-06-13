from __future__ import annotations

from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from models.action import Action


class Thought:
    def __init__(self, turn: int, actions: List[Action]):
        self.turn = turn
        self.actions = actions

    def pretty_print(self):
        print(f"Turn: {self.turn}")
        for action in self.actions:
            print(action)
