from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from constants.actions import ACTION
from models.board import Board
from models.brain import Brain
from models.deck import Deck
from models.player import Player

from services.clue_receiver import ClueReceiver
from services.player_finder import PlayerFinder

if TYPE_CHECKING:
    from models.client import Client
    from models.action import Action


class GameException(Exception):
    pass


class Game:
    def __init__(self, client: Client):
        # Meta Infos
        self.client = client
        self.table_id = None

        # Players
        self.players = []
        self.own_index = -1

        # Game fixed infos
        self.deck = None
        self.board = None
        self.suits = None

        # Game state
        self.turn_number = -1
        self.current_player_index = -1
        self.discard_pile = []
        self.clue_tokens = 8

        # Services
        self.player_finder = PlayerFinder(self)
        self.brain = Brain(self)

    def __str__(self):
        return f"Game: table_id={self.table_id}, turn_number={self.turn_number}"

    def start(self, data):
        self.generate_players(data["playerNames"])
        self.own_index = data["ourPlayerIndex"]
        self.table_id = data["tableID"]

        self.suits = [0, 1, 2, 3, 4]
        self.board = Board(self.suits)
        self.deck = Deck(self.suits)

        self.brain.set_player(self.player_finder.find_self())

    def pretty_print(self):
        print("Players:")
        for player in self.players:
            player.pretty_print()

    def generate_players(self, player_names):
        for player_index, name in enumerate(player_names):
            self.players.append(Player(name, player_index))

    def get_player(self, player_index) -> Player:
        return self.player_finder.get_player(player_index)

    def ready(self):
        self.turn_number = 0
        self.current_player_index = 0

        if self.current_player_index != self.own_index:
            return

        action_chosen = self.choose_action()
        if action_chosen in [ACTION.COLOR_CLUE, ACTION.RANK_CLUE]:
            self.clue_tokens -= 1

    def handle_action(self, data):
        try:
            if "action" in data:
                data = data["action"]
            self.update_state(data)

            if data["type"] != "turn":
                return

            if self.current_player_index != self.own_index:
                return

            print(data)
            self.choose_action()
        except Exception as e:
            print(f"Error: {e}")
            print(data)

    def status(self, data):
        if data["clues"] != self.clue_tokens:
            print(data)
            raise GameException("Clue tokens mismatch")

    def update_state(self, data):
        action = {
            "draw": self.draw,
            "play": self.play,
            "discard": self.discard,
            "clue": self.clue,
            "turn": self.turn,
            "status": self.status
        }
        action[data["type"]](data)

    def choose_action(self) -> Optional[str]:
        action = self.brain.find_action()
        self.submit_action(action)
        return action.action_type

    def draw(self, data):
        player = self.get_player(data["playerIndex"])
        player.add_card_to_hand(
            data["order"],
            data["rank"],
            data["suitIndex"],
            deck=self.deck
        )

    def play(self, data):
        player = self.get_player(data["playerIndex"])
        order = data["order"]
        card = player.remove_card_from_hand(order)
        card.set_suit(data["suitIndex"])
        card.set_rank(data["rank"])
        success = self.board.add_card(card.physical_card)
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
        self.brain.receive_clue(data=data)
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
