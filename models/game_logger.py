from __future__ import annotations

import json
import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.action import Action
    from models.game import Game


class GameLoggerException(Exception):
    pass


class GameLogger:
    def __init__(self, game: Game):
        self.game = game
        self.logs = []

    def log(self, event: dict):
        if not self.game.forced_action:
            self.logs.append(event)

    @property
    def file_name(self):
        return f"{self.game.table_id}-{self.game.player_finder.find_self().name}.json"

    def ready(self):
        self.log({'game': 'ready'})

    def start(self, data: dict):
        self.log({'start': {
            'playerNames': data['playerNames'],
            'ourPlayerIndex': data['ourPlayerIndex'],
        }})

    def action(self, action: Action):
        self.log({'action': {
            'action_type': action.action_type,
            'target': action.target,
            'value': action.value,
        }})

    def draw(self, data: dict):
        self.log({'draw': {
            'playerIndex': data['playerIndex'],
            'order': data['order'],
            'rank': data['rank'],
            'suitIndex': data['suitIndex']
        }})

    def play(self, data: dict):
        self.log({'play': {
            'playerIndex': data['playerIndex'],
            'order': data['order'],
            'rank': data['rank'],
            'suitIndex': data['suitIndex']
        }})

    def discard(self, data: dict):
        self.log({'discard': {
            'playerIndex': data['playerIndex'],
            'order': data['order'],
            'rank': data['rank'],
            'suitIndex': data['suitIndex']
        }})

    def clue(self, data: dict):
        player_index = data.get('target', data.get('player_index'))
        if "clue" in data:
            is_color_clue = data["clue"]["type"] == 0
            value = data["clue"]["value"]
        else:
            is_color_clue = data["is_color_clue"]
            value = data["value"]
        card_orders_touched = data.get('list', data.get('card_orders_touched'))
        self.log({'clue': {
            'player_index': player_index,
            'is_color_clue': is_color_clue,
            'value': value,
            'card_orders_touched': card_orders_touched
        }})

    def turn(self, data: dict):
        turn_number = data.get('num', data.get('turn_number'))
        if turn_number is None:
            raise GameLoggerException(f"No turn number in data: {data}")
        current_player_index = data.get('currentPlayerIndex', data.get('current_player_index'))
        if current_player_index is None:
            raise GameLoggerException(f"No current player index in data: {data}")

        self.log({'turn': {
            'turn_number': turn_number,
            'current_player_index': current_player_index
        }})

    def save(self):
        # Define the directory and file paths
        dir_path = os.path.join(os.getcwd(), 'game_files')
        file_path = os.path.join(dir_path, self.file_name)

        # Create the directory if it doesn't exist
        os.makedirs(dir_path, exist_ok=True)

        # Write the logs to the file in JSON format
        with open(file_path, 'w') as f:
            json.dump(self.logs, f)
