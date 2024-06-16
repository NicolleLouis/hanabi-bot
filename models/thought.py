from __future__ import annotations

import copy
from typing import List, TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from models.action import Action


class Thought:
    def __init__(self, turn: int, actions: Optional[List[Action]] = None):
        self.turn = turn
        self.actions = actions
        self.hand = None

    def set_hand(self, hand):
        self.hand = copy.deepcopy(hand)

    def pretty_print(self):
        print(f"Turn: {self.turn}")
        self.pretty_print_actions()
        self.pretty_print_hand()

    def pretty_print_actions(self):
        if self.actions is None:
            return
        print("Action: ")
        for action in self.actions:
            print(action)

    def pretty_print_hand(self):
        if self.hand is None:
            return
        print("Hand: ")
        for index in range(len(self.hand)):
            card = self.hand[-(index + 1)]
            if card.is_known:
                print(f"Slot {index + 1}: Known Card: {card.rank} of {card.suit}")
            elif card.touched:
                print(f"Slot {index + 1}: Touched Card with {len(card.computed_info.possible_cards)} possibilities")
                if len(card.computed_info.possible_cards) < 5:
                    card.computed_info.display_possibilities()
