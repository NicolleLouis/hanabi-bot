# Replay: https://hanab.live/replay/1198545
import pytest

from services.game_builder import GameBuilder

raw_data = [{"start": {"playerNames": ["LaFayetteX", "LaFayetteBot2", "LaFayetteBot1"], "ourPlayerIndex": 2}},
            {"draw": {"playerIndex": 0, "order": 0, "rank": 1, "suitIndex": 4}},
            {"draw": {"playerIndex": 0, "order": 1, "rank": 5, "suitIndex": 4}},
            {"draw": {"playerIndex": 0, "order": 2, "rank": 1, "suitIndex": 3}},
            {"draw": {"playerIndex": 0, "order": 3, "rank": 1, "suitIndex": 1}},
            {"draw": {"playerIndex": 0, "order": 4, "rank": 5, "suitIndex": 0}},
            {"draw": {"playerIndex": 1, "order": 5, "rank": 2, "suitIndex": 0}},
            {"draw": {"playerIndex": 1, "order": 6, "rank": 2, "suitIndex": 2}},
            {"draw": {"playerIndex": 1, "order": 7, "rank": 2, "suitIndex": 2}},
            {"draw": {"playerIndex": 1, "order": 8, "rank": 4, "suitIndex": 4}},
            {"draw": {"playerIndex": 1, "order": 9, "rank": 1, "suitIndex": 1}},
            {"draw": {"playerIndex": 2, "order": 10, "rank": -1, "suitIndex": -1}},
            {"draw": {"playerIndex": 2, "order": 11, "rank": -1, "suitIndex": -1}},
            {"draw": {"playerIndex": 2, "order": 12, "rank": -1, "suitIndex": -1}},
            {"draw": {"playerIndex": 2, "order": 13, "rank": -1, "suitIndex": -1}},
            {"draw": {"playerIndex": 2, "order": 14, "rank": -1, "suitIndex": -1}}, {"game": "ready"},
            {"clue": {"player_index": 1, "is_color_clue": True, "value": 1, "card_orders_touched": [9]}},
            {"turn": {"turn_number": 1, "current_player_index": 1}},
            {"clue": {"player_index": 0, "is_color_clue": False, "value": 1, "card_orders_touched": [0, 2, 3]}},
            {"turn": {"turn_number": 2, "current_player_index": 2}},
            {"action": {"action_type": 3, "target": 0, "value": 5}},
            {"clue": {"player_index": 0, "is_color_clue": False, "value": 5, "card_orders_touched": [1, 4]}},
            {"turn": {"turn_number": 3, "current_player_index": 0}},
            {"play": {"playerIndex": 0, "order": 0, "rank": 1, "suitIndex": 4}},
            {"draw": {"playerIndex": 0, "order": 15, "rank": 4, "suitIndex": 1}},
            {"turn": {"turn_number": 4, "current_player_index": 1}},
            {"play": {"playerIndex": 1, "order": 9, "rank": 1, "suitIndex": 1}},
            {"draw": {"playerIndex": 1, "order": 16, "rank": 1, "suitIndex": 2}},
            {"turn": {"turn_number": 5, "current_player_index": 2}},
            {"action": {"action_type": 3, "target": 1, "value": 1}},
            {"clue": {"player_index": 1, "is_color_clue": False, "value": 1, "card_orders_touched": [16]}},
            {"turn": {"turn_number": 6, "current_player_index": 0}},
            {"play": {"playerIndex": 0, "order": 2, "rank": 1, "suitIndex": 3}},
            {"draw": {"playerIndex": 0, "order": 17, "rank": 2, "suitIndex": 0}},
            {"turn": {"turn_number": 7, "current_player_index": 1}},
            {"play": {"playerIndex": 1, "order": 16, "rank": 1, "suitIndex": 2}},
            {"draw": {"playerIndex": 1, "order": 18, "rank": 2, "suitIndex": 1}},
            {"turn": {"turn_number": 8, "current_player_index": 2}},
            {"action": {"action_type": 2, "target": 1, "value": 1}},
            {"clue": {"player_index": 1, "is_color_clue": True, "value": 1, "card_orders_touched": [18]}},
            {"turn": {"turn_number": 9, "current_player_index": 0}},
            {"discard": {"playerIndex": 0, "order": 3, "rank": 1, "suitIndex": 1}},
            {"draw": {"playerIndex": 0, "order": 19, "rank": 4, "suitIndex": 3}},
            {"turn": {"turn_number": 10, "current_player_index": 1}},
            {"play": {"playerIndex": 1, "order": 18, "rank": 2, "suitIndex": 1}},
            {"draw": {"playerIndex": 1, "order": 20, "rank": 4, "suitIndex": 2}},
            {"turn": {"turn_number": 11, "current_player_index": 2}},
            {"action": {"action_type": 1, "target": 10, "value": None}},
            {"discard": {"playerIndex": 2, "order": 10, "rank": 4, "suitIndex": 3}},
            {"draw": {"playerIndex": 2, "order": 21, "rank": -1, "suitIndex": -1}},
            {"turn": {"turn_number": 12, "current_player_index": 0}},
            {"discard": {"playerIndex": 0, "order": 15, "rank": 4, "suitIndex": 1}},
            {"draw": {"playerIndex": 0, "order": 22, "rank": 3, "suitIndex": 3}},
            {"turn": {"turn_number": 13, "current_player_index": 1}},
            {"clue": {"player_index": 0, "is_color_clue": False, "value": 2, "card_orders_touched": [17]}},
            {"turn": {"turn_number": 14, "current_player_index": 2}},
            {"action": {"action_type": 2, "target": 0, "value": 3}},
            {"clue": {"player_index": 0, "is_color_clue": True, "value": 3, "card_orders_touched": [19, 22]}},
            {"turn": {"turn_number": 15, "current_player_index": 0}},
            {"clue": {"player_index": 2, "is_color_clue": False, "value": 1, "card_orders_touched": [11, 21]}},
            {"turn": {"turn_number": 16, "current_player_index": 1}},
            {"discard": {"playerIndex": 1, "order": 5, "rank": 2, "suitIndex": 0}},
            {"draw": {"playerIndex": 1, "order": 23, "rank": 1, "suitIndex": 4}},
            {"turn": {"turn_number": 17, "current_player_index": 2}},
            {"action": {"action_type": 0, "target": 11, "value": None}},
            {"play": {"playerIndex": 2, "order": 11, "rank": 1, "suitIndex": 0}},
            {"draw": {"playerIndex": 2, "order": 24, "rank": -1, "suitIndex": -1}},
            {"turn": {"turn_number": 18, "current_player_index": 0}},
            {"play": {"playerIndex": 0, "order": 17, "rank": 2, "suitIndex": 0}},
            {"draw": {"playerIndex": 0, "order": 25, "rank": 3, "suitIndex": 0}},
            {"turn": {"turn_number": 19, "current_player_index": 1}},
            {"clue": {"player_index": 0, "is_color_clue": True, "value": 0, "card_orders_touched": [4, 25]}},
            {"turn": {"turn_number": 20, "current_player_index": 2}}]


def test_no_crash():
    game_builder = GameBuilder(raw_data)
    game_builder.build_until_end()
    game = game_builder.export_game()
    assert game.turn_number == 20

    try:
        game.choose_action()
    except Exception as e:
        pytest.fail(f"Unexpected exception: {e}")
