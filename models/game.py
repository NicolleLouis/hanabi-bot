from __future__ import annotations

from constants.actions import ACTION
from models.brain import Brain
from models.player import Player

from typing import TYPE_CHECKING, Optional

from models.stack import Stack
from services.clue_receiver import ClueReceiver
from services.player_finder import PlayerFinder

if TYPE_CHECKING:
    from models.client import Client
    from models.action import Action


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

        self.player_finder = PlayerFinder(self)
        self.clue_receiver = ClueReceiver(self)
        self.brain = Brain(self)

    def __str__(self):
        return f"Game: table_id={self.table_id}, turn_number={self.turn_number}"

    def start(self, data):
        self.generate_players(data["playerNames"])
        self.own_index = data["ourPlayerIndex"]
        self.table_id = data["tableID"]

        suits_number = 5
        for suit in range(suits_number):
            self.stacks.append(Stack(suit))

        self.brain.set_player(self.player_finder.find_self())

    def pretty_print(self):
        print("Players:")
        for player in self.players:
            player.pretty_print()
        print("Stacks:")
        for stack in self.stacks:
            print(stack)

    def generate_players(self, player_names):
        for player_index, name in enumerate(player_names):
            self.players.append(Player(name, player_index))

    def get_player(self, player_index) -> Player:
        return self.player_finder.get_player(player_index)

    def get_stack(self, suit):
        for stack in self.stacks:
            if stack.suit == suit:
                return stack
        raise GameException(f"Stack {suit} not found")

    def ready(self):
        self.turn_number = 0
        self.current_player_index = 0
        action_chosen = self.choose_action()
        if action_chosen in [ACTION.COLOR_CLUE, ACTION.RANK_CLUE]:
            self.clue_tokens -= 1

    def handle_action(self, data):
        if "action" in data:
            data = data["action"]
        self.update_state(data)

        self.choose_action()
        print(self.clue_tokens)

    def update_state(self, data):
        action = {
            "draw": self.draw,
            "play": self.play,
            "discard": self.discard,
            "clue": self.clue,
            "turn": self.turn,
        }
        action[data["type"]](data)

    def choose_action(self) -> Optional[str]:
        if self.current_player_index != self.own_index:
            return

        action = self.brain.find_action()
        self.submit_action(action)
        return action.action_type

    def draw(self, data):
        player = self.get_player(data["playerIndex"])
        player.add_card_to_hand(
            data["order"],
            data["rank"],
            data["suitIndex"],
        )

    def play(self, data):
        player = self.get_player(data["playerIndex"])
        order = data["order"]
        card = player.remove_card_from_hand(order)
        card.set_suit(data["suitIndex"])
        card.set_rank(data["rank"])
        success = self.get_stack(card.suit).add_card(card)
        if success and card.rank == 5:
            self.clue_tokens += 1

    def discard(self, data):
        player = self.get_player(data["playerIndex"])
        order = data["order"]
        card = player.remove_card_from_hand(order)
        self.discard_pile.append(card)

        if not data["failed"]:
            self.clue_tokens += 1

    def clue(self, data):
        self.clue_receiver.receive_clue(data)
        self.clue_tokens -= 1

    def turn(self, data):
        self.turn_number = data["num"]
        self.current_player_index = data["currentPlayerIndex"]

    def submit_action(self, action: Action):
        body = {
            "tableID": self.table_id,
            "type": action.action_type,
            "target": action.target,
        }
        if action.value is not None:
            body["value"] = action.value

        self.client.send(
            "action",
            body,
        )
