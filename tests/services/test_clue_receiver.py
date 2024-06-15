from models.card.card import Card
from models.card.physical_card import PhysicalCard
from models.clue import Clue
from services.clue.clue_receiver import ClueReceiver


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


def test_compute_possible_play_cards_case_color_clue_successful(game):
    card = Card(0, -1, -1, game.deck)
    clue = Clue(
        player_index=0,
        is_color_clue=True,
        value=0,
        card_orders_touched=[0]
    )
    clue_receiver = ClueReceiver(game)
    clue_receiver.compute_possible_play_cards(card, clue)
    assert card.playable
    assert card.suit == 0
    assert card.rank == 1
    assert card.is_known


def test_compute_possible_play_cards_case_color_clue_unsuccessful(game):
    card = Card(0, -1, -1, game.deck)
    clue = Clue(
        player_index=0,
        is_color_clue=True,
        value=0,
        card_orders_touched=[0]
    )
    game.board.add_card(PhysicalCard(0, 1))
    game.board.add_card(PhysicalCard(0, 2))
    game.board.add_card(PhysicalCard(0, 3))
    game.board.add_card(PhysicalCard(0, 4))
    game.board.add_card(PhysicalCard(0, 5))

    clue_receiver = ClueReceiver(game)
    clue_receiver.compute_possible_play_cards(card, clue)
    assert not card.playable
    assert not card.is_known


def test_compute_possible_play_cards_case_rank_clue_successful(game):
    card = Card(0, -1, -1, game.deck)
    clue = Clue(
        player_index=0,
        is_color_clue=False,
        value=1,
        card_orders_touched=[0]
    )
    clue_receiver = ClueReceiver(game)
    clue_receiver.compute_possible_play_cards(card, clue)
    assert card.playable
    assert not card.is_known
    assert len(card.computed_info.possible_cards) == 5

    game.board.add_card(PhysicalCard(0, 1))
    game.board.add_card(PhysicalCard(1, 1))
    game.board.add_card(PhysicalCard(2, 1))
    game.board.add_card(PhysicalCard(3, 1))

    clue_receiver.compute_possible_play_cards(card, clue)
    assert card.playable
    assert card.is_known
    assert card.suit == 4
    assert card.rank == 1


def test_compute_possible_play_cards_case_rank_clue_unsuccessful(game):
    card = Card(0, -1, -1, game.deck)
    clue = Clue(
        player_index=0,
        is_color_clue=False,
        value=1,
        card_orders_touched=[0]
    )
    clue_receiver = ClueReceiver(game)

    game.board.add_card(PhysicalCard(0, 1))
    game.board.add_card(PhysicalCard(1, 1))
    game.board.add_card(PhysicalCard(2, 1))
    game.board.add_card(PhysicalCard(3, 1))
    game.board.add_card(PhysicalCard(4, 1))

    clue_receiver.compute_possible_play_cards(card, clue)
    assert not card.playable
