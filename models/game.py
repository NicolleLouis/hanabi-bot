from __future__ import annotations

from constants.actions import ACTION
from models.player import Player

from typing import TYPE_CHECKING

from models.stack import Stack

if TYPE_CHECKING:
    from models.client import Client


class GameException(Exception):
    pass


class Game:
    def __init__(self, client: Client):
        self.client = client
        self.table_id = None
        self.clue_tokens = 8
        self.players = []
        self.own_index = -1
        self.stacks = []
        self.discard_pile = []
        self.turn_number = -1
        self.current_player_index = -1

    def __str__(self):
        return f"Game: table_id={self.table_id}, turn_number={self.turn_number}"

    def start(self, data):
        self.generate_players(data["playerNames"])
        self.own_index = data["ourPlayerIndex"]
        self.table_id = data["tableID"]

        suits_number = 5
        for suit in range(suits_number):
            self.stacks.append(Stack(suit))

    def pretty_print(self):
        print("Players:")
        for player in self.players:
            player.pretty_print()
        print("Stacks:")
        for stack in self.stacks:
            print(stack)

    def generate_players(self, player_names):
        for i, name in enumerate(player_names):
            self.players.append(Player(name, i))

    def get_player(self, player_index) -> Player:
        return self.players[player_index]

    def get_stack(self, suit):
        for stack in self.stacks:
            if stack.suit == suit:
                return stack
        raise GameException(f"Stack {suit} not found")

    def ready(self):
        self.turn_number = 0
        self.current_player_index = 0
        self.choose_action()

    def handle_action(self, data):
        if "action" in data:
            data = data["action"]
        self.update_state(data)

        self.choose_action(data)

    def update_state(self, data):
        action = {
            "draw": self.draw,
            "play": self.play,
            "discard": self.discard,
            "clue": self.clue,
            "turn": self.turn,
        }
        action[data["type"]](data)

    # todo: refacto
    def choose_action(self, data=None):
        if self.current_player_index != self.own_index:
            return

        if self.clue_tokens > 0:
            # There is a clue available, so give a rank clue to the next
            # person's slot 1 card.

            # Target the next player.
            target_index = self.own_index + 1
            if target_index > len(self.players) - 1:
                target_index = 0

            target_player = self.get_player(target_index)
            slot_1_card = target_player.get_card_by_slot(1)

            self.send_decision(
                {
                    "type": ACTION.RANK_CLUE,
                    "target": target_index,
                    "value": slot_1_card.rank,
                }
            )
        else:
            # There are no clues available, so discard our oldest card.
            oldest_card = self.get_player(self.own_index).get_chop()
            self.send_decision(
                {
                    "type": ACTION.DISCARD,
                    "target": oldest_card.order,
                }
            )

    def draw(self, data):
        player = self.get_player(data["playerIndex"])
        player.add_card_to_hand(
            data["order"],
            data["rank"],
            data["suitIndex"],
        )

    def play(self, data):
        player = self.get_player(data["which"]["playerIndex"])
        order = data["which"]["order"]
        card = player.remove_card_from_hand(order)
        self.get_stack(card.suit).add_card(card)

    def discard(self, data):
        player = self.get_player(data["which"]["playerIndex"])
        order = data["which"]["order"]
        card = player.remove_card_from_hand(order)
        self.discard_pile.append(card)

        if not data["failed"]:
            self.clue_tokens += 1

    # ToDo send the info to the players
    def clue(self, data):
        # ['type': 'clue',
        # 'clue': {'type': 1, 'value': 1}, <- color clue
        # 'giver': 0,
        # 'list': [8, 9],
        # 'target': 1,
        # 'turn': 0}
        print(data)
        self.clue_tokens -= 1

    def turn(self, data):
        self.turn_number = data["num"]
        self.current_player_index = data["currentPlayerIndex"]

    def send_decision(self, decision):
        body = {
            "tableID": self.table_id,
            "type": decision["type"],
            "target": decision["target"],
        }
        if "value" in decision:
            body["value"] = decision["value"]

        self.client.send(
            "action",
            body,
        )
