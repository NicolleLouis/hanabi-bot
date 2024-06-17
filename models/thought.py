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
        self.touched_player_hand = None
        self.touched_player_name = None

    def set_touched_player(self, player):
        self.touched_player_hand = copy.deepcopy(player.hand)
        self.touched_player_name = player.name

    def set_hand(self, hand):
        self.hand = copy.deepcopy(hand)

    def pretty_print(self):
        print(f"Turn: {self.turn}")
        self.pretty_print_actions()
        print("Player Hand: ")
        self.pretty_print_hand(self.hand)
        print(f"{self.touched_player_name} Hand: ")
        self.pretty_print_hand(self.touched_player_hand)

    def pretty_print_actions(self):
        if self.actions is None:
            return
        print("Action: ")
        for action in self.actions:
            print(str(action))

    def pretty_print_hand(self, hand=None):
        if hand is None:
            hand = self.hand

        if hand is None:
            return
        for index in range(len(hand)):
            card = hand[-(index + 1)]
            if card.is_known:
                print(f"Slot {index + 1}: Known Card: {card.rank} of {card.suit}")
            elif card.touched:
                print(f"Slot {index + 1}: Touched Card with {len(card.computed_info.possible_cards)} possibilities")
                if len(card.computed_info.possible_cards) < 5:
                    card.computed_info.display_possibilities()
