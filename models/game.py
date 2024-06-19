from __future__ import annotations

from time import sleep
from typing import TYPE_CHECKING, Optional

from constants.actions import ACTION
from models.board import Board
from models.brain import Brain
from models.deck import Deck
from models.game_logger import GameLogger
from models.player import Player

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
        self.clue_tokens = 8

        # Services
        self.player_finder = PlayerFinder(self)
        self.brain = Brain(self)
        self.logger = GameLogger(self)

    def __str__(self):
        return f"Game: table_id={self.table_id}, turn_number={self.turn_number}"

    def start(self, data):
        self.generate_players(data["playerNames"])
        self.own_index = data["ourPlayerIndex"]
        self.table_id = data["tableID"]

        self.suits = [0, 1, 2, 3, 4]
        self.deck = Deck(self.suits)
        self.board = Board(self, self.suits)

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
        self.logger.ready()

        if self.current_player_index != self.own_index:
            return

        action_chosen = self.choose_action()
        if action_chosen.action_type in [ACTION.COLOR_CLUE, ACTION.RANK_CLUE]:
            self.brain.receive_clue(clue=action_chosen.to_clue(self))
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

            self.choose_action()
        except Exception as e:
            print(f"Error: {e}")
            print(data)

    def status(self, data):
        if data["clues"] != self.clue_tokens:
            print(data)
            print(f"Currently thought clues: {self.clue_tokens}")
            raise GameException("Clue tokens mismatch")

    def update_state(self, data):
        action = {
            "draw": self.draw,
            "play": self.play,
            "discard": self.discard,
            "clue": self.clue,
            "turn": self.turn,
            "status": self.status,
            "gameOver": self.game_over,
        }
        action[data["type"]](data)

    def game_over(self, data):
        print("Game Over")
        print(data)
        self.logger.save()

    def choose_action(self) -> Optional[Action]:
        action = self.brain.find_action()
        self.submit_action(action)
        self.logger.action(action)
        return action

    def draw(self, data):
        player = self.get_player(data["playerIndex"])
        player.add_card_to_hand(
            data["order"],
            data["rank"],
            data["suitIndex"],
            deck=self.deck
        )
        self.logger.draw(data)

    def play(self, data):
        player = self.get_player(data["playerIndex"])
        order = data["order"]
        card = player.remove_card_from_hand(order)
        card.set_suit(data["suitIndex"])
        card.set_rank(data["rank"])
        success = self.board.add_card(card.physical_card)
        if success and card.rank == 5:
            self.clue_tokens += 1
        self.logger.play(data)

    def discard(self, data):
        player = self.get_player(data["playerIndex"])
        order = data["order"]
        card = player.remove_card_from_hand(order)
        card.set_suit(data["suitIndex"])
        card.set_rank(data["rank"])
        self.board.discard_pile.append(card)

        if not data["failed"]:
            self.clue_tokens += 1
        self.logger.discard(data)

    def clue(self, data):
        self.brain.receive_clue(data=data)
        self.clue_tokens -= 1
        self.logger.clue(data)

    def turn(self, data):
        self.turn_number = data["num"]
        self.current_player_index = data["currentPlayerIndex"]
        self.brain.display_thought(self.turn_number - 1)
        self.logger.turn(data)

    def submit_action(self, action: Action):
        sleep(1)
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
