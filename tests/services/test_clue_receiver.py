from models.clue import Clue
from services.clue_receiver import ClueReceiver


def test_focus_single_touched_card_case(game):
    player = game.player_finder.get_player(0)
    player.add_card_to_hand(0, 1, 1)
    player.add_card_to_hand(1, 2, 2)
    player.add_card_to_hand(2, 1, 1)
    player.add_card_to_hand(3, 1, 1)

    clue_receiver = ClueReceiver(game)
    clue = Clue(
        player_index=0,
        is_color_clue=True,
        value=2,
        card_orders_touched=[1]
    )
    focus = clue_receiver.find_focus(clue)
    expected_focus = player.get_card(1)
    assert focus == expected_focus


def test_focus_chop_touched_case(game):
    player = game.player_finder.get_player(0)
    player.add_card_to_hand(0, 1, 1)
    player.add_card_to_hand(1, 2, 2)
    player.add_card_to_hand(2, 2, 2)
    player.add_card_to_hand(3, 1, 1)

    clue_receiver = ClueReceiver(game)
    clue = Clue(
        player_index=0,
        is_color_clue=True,
        value=1,
        card_orders_touched=[0, 3]
    )
    focus = clue_receiver.find_focus(clue)
    expected_focus = player.get_card(0)
    assert focus == expected_focus


def test_focus_multiple_new_cards(game):
    player = game.player_finder.get_player(0)
    player.add_card_to_hand(0, 1, 1)
    player.add_card_to_hand(1, 2, 2)
    player.add_card_to_hand(2, 2, 2)
    player.add_card_to_hand(3, 1, 1)

    clue_receiver = ClueReceiver(game)
    clue = Clue(
        player_index=0,
        is_color_clue=True,
        value=2,
        card_orders_touched=[1, 2]
    )
    focus = clue_receiver.find_focus(clue)
    expected_focus = player.get_card(2)
    assert focus == expected_focus


def test_focus_touched_and_untouched_case(game):
    player = game.player_finder.get_player(0)
    player.add_card_to_hand(0, 1, 1)
    player.add_card_to_hand(1, 2, 2)
    player.add_card_to_hand(2, 1, 1)
    player.add_card_to_hand(3, 1, 1)

    player.get_chop().known_info.add_positive_clue(True, 1)
    player.get_finesse().known_info.add_positive_clue(True, 1)
    clue_receiver = ClueReceiver(game)
    clue = Clue(
        player_index=0,
        is_color_clue=True,
        value=1,
        card_orders_touched=[0, 2, 3]
    )
    focus = clue_receiver.find_focus(clue)
    expected_focus = player.get_card(2)
    assert focus == expected_focus


def test_focus_only_touched_card_case(game):
    player = game.player_finder.get_player(0)
    player.add_card_to_hand(0, 1, 1)
    player.add_card_to_hand(1, 2, 2)
    player.add_card_to_hand(2, 1, 1)
    player.add_card_to_hand(3, 1, 1)

    player.get_chop().known_info.add_positive_clue(True, 1)
    player.get_card(2).known_info.add_positive_clue(True, 1)
    player.get_finesse().known_info.add_positive_clue(True, 1)
    clue_receiver = ClueReceiver(game)
    clue = Clue(
        player_index=0,
        is_color_clue=True,
        value=1,
        card_orders_touched=[0, 2, 3]
    )
    focus = clue_receiver.find_focus(clue)
    expected_focus = player.get_card(3)
    assert focus == expected_focus
