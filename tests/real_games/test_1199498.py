# https://hanab.live/replay/1199498
from models.card.physical_card import PhysicalCard
from models.clue import Clue
from services.game_builder import GameBuilder

raw_data = [{"start": {"playerNames": ["LaFayetteBot1", "LaFayetteX", "LaFayetteBot2"], "ourPlayerIndex": 0}},
            {"draw": {"playerIndex": 0, "order": 0, "rank": -1, "suitIndex": -1}},
            {"draw": {"playerIndex": 0, "order": 1, "rank": -1, "suitIndex": -1}},
            {"draw": {"playerIndex": 0, "order": 2, "rank": -1, "suitIndex": -1}},
            {"draw": {"playerIndex": 0, "order": 3, "rank": -1, "suitIndex": -1}},
            {"draw": {"playerIndex": 0, "order": 4, "rank": -1, "suitIndex": -1}},
            {"draw": {"playerIndex": 1, "order": 5, "rank": 1, "suitIndex": 3}},
            {"draw": {"playerIndex": 1, "order": 6, "rank": 3, "suitIndex": 1}},
            {"draw": {"playerIndex": 1, "order": 7, "rank": 2, "suitIndex": 2}},
            {"draw": {"playerIndex": 1, "order": 8, "rank": 2, "suitIndex": 1}},
            {"draw": {"playerIndex": 1, "order": 9, "rank": 2, "suitIndex": 2}},
            {"draw": {"playerIndex": 2, "order": 10, "rank": 4, "suitIndex": 1}},
            {"draw": {"playerIndex": 2, "order": 11, "rank": 3, "suitIndex": 3}},
            {"draw": {"playerIndex": 2, "order": 12, "rank": 1, "suitIndex": 1}},
            {"draw": {"playerIndex": 2, "order": 13, "rank": 3, "suitIndex": 1}},
            {"draw": {"playerIndex": 2, "order": 14, "rank": 4, "suitIndex": 3}}, {"game": "ready"},
            {"action": {"action_type": 3, "target": 2, "value": 1}},
            {"turn": {"turn_number": 1, "current_player_index": 1}},
            {"clue": {"player_index": 0, "is_color_clue": False, "value": 1, "card_orders_touched": [0, 3, 4]}},
            {"turn": {"turn_number": 2, "current_player_index": 2}},
            {"play": {"playerIndex": 2, "order": 12, "rank": 1, "suitIndex": 1}},
            {"draw": {"playerIndex": 2, "order": 15, "rank": 3, "suitIndex": 4}},
            {"turn": {"turn_number": 3, "current_player_index": 0}},
            {"action": {"action_type": 0, "target": 0, "value": None}},
            {"play": {"playerIndex": 0, "order": 0, "rank": 1, "suitIndex": 0}},
            {"draw": {"playerIndex": 0, "order": 16, "rank": -1, "suitIndex": -1}},
            {"turn": {"turn_number": 4, "current_player_index": 1}},
            {"clue": {"player_index": 0, "is_color_clue": True, "value": 3, "card_orders_touched": [2, 3]}},
            {"turn": {"turn_number": 5, "current_player_index": 2}},
            {"clue": {"player_index": 1, "is_color_clue": True, "value": 1, "card_orders_touched": [6, 8]}},
            {"turn": {"turn_number": 6, "current_player_index": 0}},
            {"action": {"action_type": 0, "target": 4, "value": None}},
            {"play": {"playerIndex": 0, "order": 4, "rank": 1, "suitIndex": 2}},
            {"draw": {"playerIndex": 0, "order": 17, "rank": -1, "suitIndex": -1}},
            {"turn": {"turn_number": 7, "current_player_index": 1}},
            {"play": {"playerIndex": 1, "order": 8, "rank": 2, "suitIndex": 1}},
            {"draw": {"playerIndex": 1, "order": 18, "rank": 3, "suitIndex": 0}},
            {"turn": {"turn_number": 8, "current_player_index": 2}},
            {"discard": {"playerIndex": 2, "order": 10, "rank": 4, "suitIndex": 1}},
            {"draw": {"playerIndex": 2, "order": 19, "rank": 3, "suitIndex": 4}},
            {"turn": {"turn_number": 9, "current_player_index": 0}},
            {"action": {"action_type": 0, "target": 2, "value": None}},
            {"draw": {"playerIndex": 0, "order": 20, "rank": -1, "suitIndex": -1}},
            {"turn": {"turn_number": 10, "current_player_index": 1}}]


def test_turn_5_should_understand_b2():
    game_builder = GameBuilder(raw_data)
    game_builder.build_until_turn(4)
    game = game_builder.game

    clue = Clue(
        player_index=0,
        is_color_clue=True,
        value=3,
        card_orders_touched=[2, 3]
    )
    game.brain.receive_clue(clue=clue)

    player = game.player_finder.find_self()
    remaining_1 = player.get_card_by_slot(2)
    blue_1 = player.get_card_by_slot(3)
    blue_2 = player.get_card_by_slot(4)

    possible_cards = remaining_1.computed_info.possible_cards
    assert len(possible_cards) == 2
    assert PhysicalCard(2, 1) in possible_cards
    assert PhysicalCard(4, 1) in possible_cards

    assert blue_1.is_known
    assert blue_1.suit == 3
    assert blue_1.rank == 1

    assert blue_2.is_known
    assert blue_2.suit == 3
    assert blue_2.rank == 2
