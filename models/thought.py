from __future__ import annotations

from typing import List, TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from models.action import Action


class Thought:
    def __init__(self, turn: int, actions: Optional[List[Action]] = None):
        self.turn = turn
        self.actions = actions
        self.hand = None

    def pretty_print(self):
        print(f"Turn: {self.turn}")
        if self.actions is not None:
            print("Action: ")
            for action in self.actions:
                print(action)
        if self.hand is not None:
            print("Hand: ")
            for card in self.hand:
                card.pretty_print()
