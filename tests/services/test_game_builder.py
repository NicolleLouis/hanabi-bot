from models.action import Action
from models.game import Game
from services.game_builder import GameBuilder

raw_data = [
    {
        "start": {
            "playerNames": [
                "LaFayetteBot1",
                "LaFayetteX",
                "LaFayetteBot2"
            ],
            "ourPlayerIndex": 0
        }
    },
    {
        "draw": {
            "playerIndex": 0,
            "order": 0,
            "rank": -1,
            "suitIndex": -1
        }
    },
    {
        "draw": {
            "playerIndex": 0,
            "order": 1,
            "rank": -1,
            "suitIndex": -1
        }
    },
    {
        "draw": {
            "playerIndex": 0,
            "order": 2,
            "rank": -1,
            "suitIndex": -1
        }
    },
    {
        "draw": {
            "playerIndex": 0,
            "order": 3,
            "rank": -1,
            "suitIndex": -1
        }
    },
    {
        "draw": {
            "playerIndex": 0,
            "order": 4,
            "rank": -1,
            "suitIndex": -1
        }
    },
    {
        "draw": {
            "playerIndex": 1,
            "order": 5,
            "rank": 3,
            "suitIndex": 1
        }
    },
    {
        "draw": {
            "playerIndex": 1,
            "order": 6,
            "rank": 2,
            "suitIndex": 0
        }
    },
    {
        "draw": {
            "playerIndex": 1,
            "order": 7,
            "rank": 3,
            "suitIndex": 0
        }
    },
    {
        "draw": {
            "playerIndex": 1,
            "order": 8,
            "rank": 1,
            "suitIndex": 3
        }
    },
    {
        "draw": {
            "playerIndex": 1,
            "order": 9,
            "rank": 4,
            "suitIndex": 2
        }
    },
    {
        "draw": {
            "playerIndex": 2,
            "order": 10,
            "rank": 2,
            "suitIndex": 1
        }
    },
    {
        "draw": {
            "playerIndex": 2,
            "order": 11,
            "rank": 4,
            "suitIndex": 1
        }
    },
    {
        "draw": {
            "playerIndex": 2,
            "order": 12,
            "rank": 1,
            "suitIndex": 3
        }
    },
    {
        "draw": {
            "playerIndex": 2,
            "order": 13,
            "rank": 2,
            "suitIndex": 2
        }
    },
    {
        "draw": {
            "playerIndex": 2,
            "order": 14,
            "rank": 2,
            "suitIndex": 2
        }
    },
    {
        "game": "ready"
    },
    {
        "action": {
            "action_type": 3,
            "target": 1,
            "value": 1
        }
    },
    {
        "turn": {
            "turn_number": 1,
            "current_player_index": 1
        }
    },
    {
        "play": {
            "playerIndex": 1,
            "order": 8,
            "rank": 1,
            "suitIndex": 3
        }
    },
    {
        "draw": {
            "playerIndex": 1,
            "order": 15,
            "rank": 1,
            "suitIndex": 1
        }
    },
    {
        "turn": {
            "turn_number": 2,
            "current_player_index": 2
        }
    },
    {
        "clue": {
            "player_index": 1,
            "is_color_clue": False,
            "value": 1,
            "card_orders_touched": [
                15
            ]
        }
    },
    {
        "turn": {
            "turn_number": 3,
            "current_player_index": 0
        }
    },
    {
        "action": {
            "action_type": 1,
            "target": 0,
            "value": None
        }
    },
    {
        "discard": {
            "playerIndex": 0,
            "order": 0,
            "rank": 3,
            "suitIndex": 0
        }
    },
    {
        "draw": {
            "playerIndex": 0,
            "order": 16,
            "rank": -1,
            "suitIndex": -1
        }
    },
    {
        "turn": {
            "turn_number": 4,
            "current_player_index": 1
        }
    },
    {
        "play": {
            "playerIndex": 1,
            "order": 15,
            "rank": 1,
            "suitIndex": 1
        }
    },
    {
        "draw": {
            "playerIndex": 1,
            "order": 17,
            "rank": 4,
            "suitIndex": 4
        }
    },
    {
        "turn": {
            "turn_number": 5,
            "current_player_index": 2
        }
    },
    {
        "clue": {
            "player_index": 0,
            "is_color_clue": False,
            "value": 5,
            "card_orders_touched": [
                1,
                4
            ]
        }
    },
    {
        "turn": {
            "turn_number": 6,
            "current_player_index": 0
        }
    },
    {
        "action": {
            "action_type": 2,
            "target": 2,
            "value": 1
        }
    },
    {
        "clue": {
            "player_index": 2,
            "is_color_clue": True,
            "value": 1,
            "card_orders_touched": [
                10,
                11
            ]
        }
    },
    {
        "turn": {
            "turn_number": 7,
            "current_player_index": 1
        }
    },
    {
        "clue": {
            "player_index": 0,
            "is_color_clue": False,
            "value": 2,
            "card_orders_touched": [
                16
            ]
        }
    },
    {
        "turn": {
            "turn_number": 8,
            "current_player_index": 2
        }
    },
    {
        "play": {
            "playerIndex": 2,
            "order": 10,
            "rank": 2,
            "suitIndex": 1
        }
    },
    {
        "draw": {
            "playerIndex": 2,
            "order": 18,
            "rank": 3,
            "suitIndex": 4
        }
    },
    {
        "turn": {
            "turn_number": 9,
            "current_player_index": 0
        }
    },
    {
        "action": {
            "action_type": 0,
            "target": 16,
            "value": None
        }
    },
    {
        "play": {
            "playerIndex": 0,
            "order": 16,
            "rank": 2,
            "suitIndex": 3
        }
    },
    {
        "draw": {
            "playerIndex": 0,
            "order": 19,
            "rank": -1,
            "suitIndex": -1
        }
    },
    {
        "turn": {
            "turn_number": 10,
            "current_player_index": 1
        }
    },
    {
        "clue": {
            "player_index": 0,
            "is_color_clue": True,
            "value": 1,
            "card_orders_touched": [
                2,
                4
            ]
        }
    },
    {
        "turn": {
            "turn_number": 11,
            "current_player_index": 2
        }
    },
    {
        "discard": {
            "playerIndex": 2,
            "order": 12,
            "rank": 1,
            "suitIndex": 3
        }
    },
    {
        "draw": {
            "playerIndex": 2,
            "order": 20,
            "rank": 4,
            "suitIndex": 1
        }
    },
    {
        "turn": {
            "turn_number": 12,
            "current_player_index": 0
        }
    },
    {
        "action": {
            "action_type": 0,
            "target": 2,
            "value": None
        }
    },
    {
        "play": {
            "playerIndex": 0,
            "order": 2,
            "rank": 3,
            "suitIndex": 1
        }
    },
    {
        "draw": {
            "playerIndex": 0,
            "order": 21,
            "rank": -1,
            "suitIndex": -1
        }
    },
    {
        "turn": {
            "turn_number": 13,
            "current_player_index": 1
        }
    },
    {
        "discard": {
            "playerIndex": 1,
            "order": 5,
            "rank": 3,
            "suitIndex": 1
        }
    },
    {
        "draw": {
            "playerIndex": 1,
            "order": 22,
            "rank": 5,
            "suitIndex": 4
        }
    },
    {
        "turn": {
            "turn_number": 14,
            "current_player_index": 2
        }
    },
    {
        "play": {
            "playerIndex": 2,
            "order": 11,
            "rank": 4,
            "suitIndex": 1
        }
    },
    {
        "draw": {
            "playerIndex": 2,
            "order": 23,
            "rank": 1,
            "suitIndex": 0
        }
    },
    {
        "turn": {
            "turn_number": 15,
            "current_player_index": 0
        }
    },
    {
        "action": {
            "action_type": 0,
            "target": 4,
            "value": None
        }
    },
    {
        "play": {
            "playerIndex": 0,
            "order": 4,
            "rank": 5,
            "suitIndex": 1
        }
    },
    {
        "draw": {
            "playerIndex": 0,
            "order": 24,
            "rank": -1,
            "suitIndex": -1
        }
    },
    {
        "turn": {
            "turn_number": 16,
            "current_player_index": 1
        }
    },
    {
        "clue": {
            "player_index": 2,
            "is_color_clue": True,
            "value": 0,
            "card_orders_touched": [
                23
            ]
        }
    },
    {
        "turn": {
            "turn_number": 17,
            "current_player_index": 2
        }
    },
    {
        "clue": {
            "player_index": 0,
            "is_color_clue": True,
            "value": 4,
            "card_orders_touched": [
                19,
                24
            ]
        }
    },
    {
        "turn": {
            "turn_number": 18,
            "current_player_index": 0
        }
    },
    {
        "action": {
            "action_type": 0,
            "target": 24,
            "value": None
        }
    },
    {
        "play": {
            "playerIndex": 0,
            "order": 24,
            "rank": 1,
            "suitIndex": 4
        }
    },
    {
        "draw": {
            "playerIndex": 0,
            "order": 25,
            "rank": -1,
            "suitIndex": -1
        }
    },
    {
        "turn": {
            "turn_number": 19,
            "current_player_index": 1
        }
    },
    {
        "discard": {
            "playerIndex": 1,
            "order": 6,
            "rank": 2,
            "suitIndex": 0
        }
    },
    {
        "draw": {
            "playerIndex": 1,
            "order": 26,
            "rank": 1,
            "suitIndex": 1
        }
    },
    {
        "turn": {
            "turn_number": 20,
            "current_player_index": 2
        }
    },
    {
        "play": {
            "playerIndex": 2,
            "order": 23,
            "rank": 1,
            "suitIndex": 0
        }
    },
    {
        "draw": {
            "playerIndex": 2,
            "order": 27,
            "rank": 3,
            "suitIndex": 3
        }
    },
    {
        "turn": {
            "turn_number": 21,
            "current_player_index": 0
        }
    },
    {
        "action": {
            "action_type": 2,
            "target": 2,
            "value": 3
        }
    },
    {
        "clue": {
            "player_index": 2,
            "is_color_clue": True,
            "value": 3,
            "card_orders_touched": [
                27
            ]
        }
    },
    {
        "turn": {
            "turn_number": 22,
            "current_player_index": 1
        }
    },
    {
        "clue": {
            "player_index": 0,
            "is_color_clue": False,
            "value": 4,
            "card_orders_touched": [
                19,
                21
            ]
        }
    },
    {
        "turn": {
            "turn_number": 23,
            "current_player_index": 2
        }
    },
    {
        "play": {
            "playerIndex": 2,
            "order": 27,
            "rank": 3,
            "suitIndex": 3
        }
    },
    {
        "draw": {
            "playerIndex": 2,
            "order": 28,
            "rank": 1,
            "suitIndex": 1
        }
    },
    {
        "turn": {
            "turn_number": 24,
            "current_player_index": 0
        }
    },
    {
        "action": {
            "action_type": 3,
            "target": 1,
            "value": 3
        }
    },
    {
        "clue": {
            "player_index": 1,
            "is_color_clue": False,
            "value": 3,
            "card_orders_touched": [
                7
            ]
        }
    },
    {
        "turn": {
            "turn_number": 25,
            "current_player_index": 1
        }
    },
    {
        "discard": {
            "playerIndex": 1,
            "order": 9,
            "rank": 4,
            "suitIndex": 2
        }
    },
    {
        "draw": {
            "playerIndex": 1,
            "order": 29,
            "rank": 3,
            "suitIndex": 2
        }
    },
    {
        "turn": {
            "turn_number": 26,
            "current_player_index": 2
        }
    },
    {
        "discard": {
            "playerIndex": 2,
            "order": 13,
            "rank": 2,
            "suitIndex": 2
        }
    },
    {
        "draw": {
            "playerIndex": 2,
            "order": 30,
            "rank": 3,
            "suitIndex": 3
        }
    },
    {
        "turn": {
            "turn_number": 27,
            "current_player_index": 0
        }
    },
    {
        "action": {
            "action_type": 2,
            "target": 2,
            "value": 2
        }
    },
    {
        "clue": {
            "player_index": 2,
            "is_color_clue": True,
            "value": 2,
            "card_orders_touched": [
                14
            ]
        }
    },
    {
        "turn": {
            "turn_number": 28,
            "current_player_index": 1
        }
    },
    {
        "discard": {
            "playerIndex": 1,
            "order": 17,
            "rank": 4,
            "suitIndex": 4
        }
    },
    {
        "draw": {
            "playerIndex": 1,
            "order": 31,
            "rank": 1,
            "suitIndex": 2
        }
    },
    {
        "turn": {
            "turn_number": 29,
            "current_player_index": 2
        }
    },
    {
        "clue": {
            "player_index": 1,
            "is_color_clue": False,
            "value": 5,
            "card_orders_touched": [
                22
            ]
        }
    },
    {
        "turn": {
            "turn_number": 30,
            "current_player_index": 0
        }
    },
    {
        "action": {
            "action_type": 1,
            "target": 3,
            "value": None
        }
    },
    {
        "discard": {
            "playerIndex": 0,
            "order": 3,
            "rank": 1,
            "suitIndex": 3
        }
    },
    {
        "draw": {
            "playerIndex": 0,
            "order": 32,
            "rank": -1,
            "suitIndex": -1
        }
    },
    {
        "turn": {
            "turn_number": 31,
            "current_player_index": 1
        }
    },
    {
        "clue": {
            "player_index": 0,
            "is_color_clue": True,
            "value": 3,
            "card_orders_touched": [
                21
            ]
        }
    },
    {
        "turn": {
            "turn_number": 32,
            "current_player_index": 2
        }
    },
    {
        "discard": {
            "playerIndex": 2,
            "order": 18,
            "rank": 3,
            "suitIndex": 4
        }
    },
    {
        "draw": {
            "playerIndex": 2,
            "order": 33,
            "rank": 3,
            "suitIndex": 2
        }
    },
    {
        "turn": {
            "turn_number": 33,
            "current_player_index": 0
        }
    },
    {
        "action": {
            "action_type": 0,
            "target": 21,
            "value": None
        }
    },
    {
        "play": {
            "playerIndex": 0,
            "order": 21,
            "rank": 4,
            "suitIndex": 3
        }
    },
    {
        "draw": {
            "playerIndex": 0,
            "order": 34,
            "rank": -1,
            "suitIndex": -1
        }
    },
    {
        "turn": {
            "turn_number": 34,
            "current_player_index": 1
        }
    },
    {
        "clue": {
            "player_index": 0,
            "is_color_clue": False,
            "value": 3,
            "card_orders_touched": [
                25
            ]
        }
    },
    {
        "turn": {
            "turn_number": 35,
            "current_player_index": 2
        }
    },
    {
        "clue": {
            "player_index": 0,
            "is_color_clue": False,
            "value": 4,
            "card_orders_touched": [
                19,
                32
            ]
        }
    },
    {
        "turn": {
            "turn_number": 36,
            "current_player_index": 0
        }
    },
    {
        "action": {
            "action_type": 1,
            "target": 34,
            "value": None
        }
    },
    {
        "discard": {
            "playerIndex": 0,
            "order": 34,
            "rank": 1,
            "suitIndex": 4
        }
    },
    {
        "draw": {
            "playerIndex": 0,
            "order": 35,
            "rank": -1,
            "suitIndex": -1
        }
    },
    {
        "turn": {
            "turn_number": 37,
            "current_player_index": 1
        }
    },
    {
        "discard": {
            "playerIndex": 1,
            "order": 26,
            "rank": 1,
            "suitIndex": 1
        }
    },
    {
        "draw": {
            "playerIndex": 1,
            "order": 36,
            "rank": 2,
            "suitIndex": 0
        }
    },
    {
        "turn": {
            "turn_number": 38,
            "current_player_index": 2
        }
    },
    {
        "clue": {
            "player_index": 1,
            "is_color_clue": False,
            "value": 1,
            "card_orders_touched": [
                31
            ]
        }
    },
    {
        "turn": {
            "turn_number": 39,
            "current_player_index": 0
        }
    },
    {
        "action": {
            "action_type": 1,
            "target": 35,
            "value": None
        }
    },
    {
        "discard": {
            "playerIndex": 0,
            "order": 35,
            "rank": 1,
            "suitIndex": 4
        }
    },
    {
        "draw": {
            "playerIndex": 0,
            "order": 37,
            "rank": -1,
            "suitIndex": -1
        }
    },
    {
        "turn": {
            "turn_number": 40,
            "current_player_index": 1
        }
    },
    {
        "play": {
            "playerIndex": 1,
            "order": 31,
            "rank": 1,
            "suitIndex": 2
        }
    },
    {
        "draw": {
            "playerIndex": 1,
            "order": 38,
            "rank": 1,
            "suitIndex": 0
        }
    },
    {
        "turn": {
            "turn_number": 41,
            "current_player_index": 2
        }
    },
    {
        "play": {
            "playerIndex": 2,
            "order": 14,
            "rank": 2,
            "suitIndex": 2
        }
    },
    {
        "draw": {
            "playerIndex": 2,
            "order": 39,
            "rank": 2,
            "suitIndex": 1
        }
    },
    {
        "turn": {
            "turn_number": 42,
            "current_player_index": 0
        }
    },
    {
        "action": {
            "action_type": 1,
            "target": 37,
            "value": None
        }
    },
    {
        "discard": {
            "playerIndex": 0,
            "order": 37,
            "rank": 4,
            "suitIndex": 0
        }
    },
    {
        "draw": {
            "playerIndex": 0,
            "order": 40,
            "rank": -1,
            "suitIndex": -1
        }
    },
    {
        "turn": {
            "turn_number": 43,
            "current_player_index": 1
        }
    },
    {
        "clue": {
            "player_index": 2,
            "is_color_clue": True,
            "value": 2,
            "card_orders_touched": [
                33
            ]
        }
    },
    {
        "turn": {
            "turn_number": 44,
            "current_player_index": 2
        }
    },
    {
        "play": {
            "playerIndex": 2,
            "order": 33,
            "rank": 3,
            "suitIndex": 2
        }
    },
    {
        "draw": {
            "playerIndex": 2,
            "order": 41,
            "rank": 5,
            "suitIndex": 3
        }
    },
    {
        "turn": {
            "turn_number": 45,
            "current_player_index": 0
        }
    },
    {
        "action": {
            "action_type": 1,
            "target": 40,
            "value": None
        }
    },
    {
        "discard": {
            "playerIndex": 0,
            "order": 40,
            "rank": 1,
            "suitIndex": 2
        }
    },
    {
        "draw": {
            "playerIndex": 0,
            "order": 42,
            "rank": -1,
            "suitIndex": -1
        }
    },
    {
        "turn": {
            "turn_number": 46,
            "current_player_index": 1
        }
    },
    {
        "clue": {
            "player_index": 0,
            "is_color_clue": True,
            "value": 2,
            "card_orders_touched": [
                32,
                42
            ]
        }
    },
    {
        "turn": {
            "turn_number": 47,
            "current_player_index": 2
        }
    },
    {
        "discard": {
            "playerIndex": 2,
            "order": 20,
            "rank": 4,
            "suitIndex": 1
        }
    },
    {
        "draw": {
            "playerIndex": 2,
            "order": 43,
            "rank": 4,
            "suitIndex": 0
        }
    },
    {
        "turn": {
            "turn_number": 48,
            "current_player_index": 0
        }
    },
    {
        "action": {
            "action_type": 0,
            "target": 32,
            "value": None
        }
    },
    {
        "play": {
            "playerIndex": 0,
            "order": 32,
            "rank": 4,
            "suitIndex": 2
        }
    },
    {
        "draw": {
            "playerIndex": 0,
            "order": 44,
            "rank": -1,
            "suitIndex": -1
        }
    },
    {
        "turn": {
            "turn_number": 49,
            "current_player_index": 1
        }
    },
    {
        "clue": {
            "player_index": 0,
            "is_color_clue": True,
            "value": 4,
            "card_orders_touched": [
                19,
                25,
                44
            ]
        }
    },
    {
        "turn": {
            "turn_number": 50,
            "current_player_index": 2
        }
    },
    {
        "discard": {
            "playerIndex": 2,
            "order": 28,
            "rank": 1,
            "suitIndex": 1
        }
    },
    {
        "draw": {
            "playerIndex": 2,
            "order": 45,
            "rank": 2,
            "suitIndex": 3
        }
    },
    {
        "turn": {
            "turn_number": 51,
            "current_player_index": 0
        }
    },
    {
        "action": {
            "action_type": 1,
            "target": 42,
            "value": None
        }
    },
    {
        "discard": {
            "playerIndex": 0,
            "order": 42,
            "rank": 5,
            "suitIndex": 2
        }
    },
    {
        "draw": {
            "playerIndex": 0,
            "order": 46,
            "rank": -1,
            "suitIndex": -1
        }
    },
    {
        "turn": {
            "turn_number": 52,
            "current_player_index": 1
        }
    },
    {
        "clue": {
            "player_index": 2,
            "is_color_clue": False,
            "value": 5,
            "card_orders_touched": [
                41
            ]
        }
    },
    {
        "turn": {
            "turn_number": 53,
            "current_player_index": 2
        }
    },
    {
        "play": {
            "playerIndex": 2,
            "order": 41,
            "rank": 5,
            "suitIndex": 3
        }
    },
    {
        "draw": {
            "playerIndex": 2,
            "order": 47,
            "rank": 4,
            "suitIndex": 3
        }
    },
    {
        "turn": {
            "turn_number": 54,
            "current_player_index": 0
        }
    },
    {
        "action": {
            "action_type": 1,
            "target": 46,
            "value": None
        }
    },
    {
        "discard": {
            "playerIndex": 0,
            "order": 46,
            "rank": 1,
            "suitIndex": 0
        }
    },
    {
        "draw": {
            "playerIndex": 0,
            "order": 48,
            "rank": -1,
            "suitIndex": -1
        }
    },
    {
        "turn": {
            "turn_number": 55,
            "current_player_index": 1
        }
    },
    {
        "play": {
            "playerIndex": 1,
            "order": 36,
            "rank": 2,
            "suitIndex": 0
        }
    },
    {
        "draw": {
            "playerIndex": 1,
            "order": 49,
            "rank": 1,
            "suitIndex": 2
        }
    },
    {
        "turn": {
            "turn_number": 56,
            "current_player_index": 2
        }
    },
    {
        "discard": {
            "playerIndex": 2,
            "order": 30,
            "rank": 3,
            "suitIndex": 3
        }
    },
    {
        "turn": {
            "turn_number": 57,
            "current_player_index": 0
        }
    },
    {
        "action": {
            "action_type": 3,
            "target": 1,
            "value": 5
        }
    },
    {
        "clue": {
            "player_index": 1,
            "is_color_clue": False,
            "value": 5,
            "card_orders_touched": [
                22
            ]
        }
    },
    {
        "turn": {
            "turn_number": 58,
            "current_player_index": 1
        }
    },
    {
        "play": {
            "playerIndex": 1,
            "order": 7,
            "rank": 3,
            "suitIndex": 0
        }
    }
]


def test_export():
    game = GameBuilder(raw_data).export_game()
    assert isinstance(game, Game)
    assert not game.forced_action


def test_set_next_action():
    game_builder = GameBuilder(raw_data)
    assert game_builder.next_action is None

    game_builder.next_action = 1
    game_builder.set_next_action()
    assert game_builder.next_action == 1

    game_builder.next_action = None
    game_builder.set_next_action()
    expected_result = Action(
        action_type=3,
        target=1,
        value=1
    )
    assert game_builder.next_action == expected_result


def test_get_next_action():
    game_builder = GameBuilder(raw_data)
    assert game_builder.next_action is None
    expected_result = Action(
        action_type=3,
        target=1,
        value=1
    )
    assert game_builder.get_next_action() == expected_result
    assert game_builder.next_action is None


def test_get_next_event():
    game_builder = GameBuilder(raw_data)
    initial_event_number = len(game_builder.raw_data)
    expected_result = game_builder.raw_data[0]
    event = game_builder.get_next_event()

    assert len(game_builder.raw_data) == initial_event_number - 1
    assert event == expected_result


def test_build_until_turn():
    game_builder = GameBuilder(raw_data)
    game_builder.build_until_turn(10)
    assert game_builder.game.turn_number == 10

    print("GameBuilder: build_until_turn() passed")