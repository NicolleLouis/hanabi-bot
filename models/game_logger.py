from __future__ import annotations

import json
import os
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from models.action import Action
    from models.game import Game


class GameLogger:
    def __init__(self, game: Game):
        self.game = game
        self.logs = []

    def log(self, event: dict):
        self.logs.append(event)

    @property
    def file_name(self):
        return f"{self.game.table_id}-{self.game.player_finder.find_self().name}.json"

    def ready(self):
        self.log({'game': 'ready'})

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
        self.log({'clue': {
            'player_index': data['target'],
            'is_color_clue': data['clue']['type'] == 0,
            'value': data['clue']['value'],
            'card_orders_touched': data['list']
        }})

    def turn(self, data: dict):
        self.log({'turn': {
            'turn_number': data['num'],
            'current_player_index': data['currentPlayerIndex']
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
