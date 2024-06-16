from unittest.mock import patch

from models.card.card import Card
from models.card.physical_card import PhysicalCard
from models.clue import Clue
from services.card import CardService
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


@patch.object(ClueReceiver, "is_legal_save_clue", return_value=True)
@patch.object(ClueReceiver, "get_possible_save_cards", return_value=[])
def test_compute_possible_save_cards_case_error(
        _mock_is_legal_save_clue,
        _mock_get_possible_save_cards,
        game
):
    card = Card(0, -1, -1, game.deck)
    clue = Clue(
        player_index=0,
        is_color_clue=False,
        value=1,
        card_orders_touched=[0]
    )
    clue_receiver = ClueReceiver(game)
    clue_receiver.compute_possible_save_cards(card, clue)
    assert not card.is_known
    assert len(card.computed_info.possible_cards) == 25


@patch.object(ClueReceiver, "is_legal_save_clue", return_value=False)
@patch.object(ClueReceiver, "compute_possible_play_cards")
def test_compute_possible_save_cards_case_error(
        _mock_is_legal_save_clue,
        mock_compute_possible_play_cards,
        game
):
    card = Card(0, -1, -1, game.deck)
    clue = Clue(
        player_index=0,
        is_color_clue=False,
        value=1,
        card_orders_touched=[0]
    )
    clue_receiver = ClueReceiver(game)
    clue_receiver.compute_possible_save_cards(card, clue)
    mock_compute_possible_play_cards.assert_called_once()


@patch.object(ClueReceiver, "is_legal_save_clue", return_value=True)
@patch.object(ClueReceiver, "get_possible_save_cards", return_value=[
    PhysicalCard(0, 1)
])
def test_compute_possible_save_cards_case_single_option(
        _mock_is_legal_save_clue,
        mock_get_possible_save_cards,
        game
):
    card = Card(0, -1, -1, game.deck)
    clue = Clue(
        player_index=0,
        is_color_clue=False,
        value=1,
        card_orders_touched=[0]
    )
    clue_receiver = ClueReceiver(game)
    clue_receiver.compute_possible_save_cards(card, clue)
    assert card.is_known
    assert card.suit == 0
    assert card.rank == 1


@patch.object(ClueReceiver, "is_legal_save_clue", return_value=True)
@patch.object(ClueReceiver, "get_possible_save_cards", return_value=[
    PhysicalCard(0, 1),
    PhysicalCard(1, 1),
])
def test_compute_possible_save_cards_case_multiple_option(
        _mock_is_legal_save_clue,
        mock_get_possible_save_cards,
        game
):
    card = Card(0, -1, -1, game.deck)
    clue = Clue(
        player_index=0,
        is_color_clue=False,
        value=1,
        card_orders_touched=[0]
    )
    clue_receiver = ClueReceiver(game)
    clue_receiver.compute_possible_save_cards(card, clue)
    assert not card.is_known
    assert len(card.computed_info.possible_cards) == 2
    assert PhysicalCard(0, 1) in card.computed_info.possible_cards
    assert PhysicalCard(1, 1) in card.computed_info.possible_cards


def test_get_possible_save_cards_case_color(game):
    game.board.discard_pile.append(Card(0, 0, 3, game.deck))
    game.board.discard_pile.append(Card(1, 0, 5, game.deck))
    clue_receiver = ClueReceiver(game)
    clue = Clue(
        player_index=0,
        is_color_clue=True,
        value=0,
        card_orders_touched=[0, 1]
    )
    save_cards = clue_receiver.get_possible_save_cards(clue)
    save_cards = CardService.convert_to_physical_cards(save_cards)
    assert len(save_cards) == 1
    assert PhysicalCard(0, 3) in save_cards


def test_get_possible_save_cards_case_rank_5(game):
    clue_receiver = ClueReceiver(game)
    clue = Clue(
        player_index=0,
        is_color_clue=False,
        value=5,
        card_orders_touched=[0, 1]
    )
    save_cards = clue_receiver.get_possible_save_cards(clue)
    save_cards = CardService.convert_to_physical_cards(save_cards)
    assert len(save_cards) == 5
    assert PhysicalCard(0, 5) in save_cards
    assert PhysicalCard(1, 5) in save_cards
    assert PhysicalCard(2, 5) in save_cards
    assert PhysicalCard(3, 5) in save_cards
    assert PhysicalCard(4, 5) in save_cards


def test_get_possible_save_cards_case_rank_2(game):
    clue_receiver = ClueReceiver(game)
    clue = Clue(
        player_index=0,
        is_color_clue=False,
        value=2,
        card_orders_touched=[0, 1]
    )
    save_cards = clue_receiver.get_possible_save_cards(clue)
    save_cards = CardService.convert_to_physical_cards(save_cards)
    assert len(set(save_cards)) == 5
    assert PhysicalCard(0, 2) in save_cards
    assert PhysicalCard(1, 2) in save_cards
    assert PhysicalCard(2, 2) in save_cards
    assert PhysicalCard(3, 2) in save_cards
    assert PhysicalCard(4, 2) in save_cards


def test_get_possible_save_cards_case_rank_3_or_4(game):
    game.board.discard_pile.append(Card(0, 0, 3, game.deck))
    game.board.discard_pile.append(Card(1, 0, 4, game.deck))
    clue_receiver = ClueReceiver(game)
    clue = Clue(
        player_index=0,
        is_color_clue=False,
        value=3,
        card_orders_touched=[0, 1]
    )
    save_cards = clue_receiver.get_possible_save_cards(clue)
    save_cards = CardService.convert_to_physical_cards(save_cards)
    assert len(save_cards) == 1
    assert PhysicalCard(0, 3) in save_cards


def test_is_legal_save_color_clue(game):
    clue_receiver = ClueReceiver(game)
    clue = Clue(
        player_index=0,
        is_color_clue=True,
        value=0,
        card_orders_touched=[0]
    )
    assert not clue_receiver.is_legal_save_color_clue(clue)

    game.board.discard_pile.append(Card(1, 0, 1, game.deck))
    assert not clue_receiver.is_legal_save_color_clue(clue)

    game.board.discard_pile.append(Card(2, 0, 3, game.deck))
    assert clue_receiver.is_legal_save_color_clue(clue)

    game.board.add_card(PhysicalCard(0, 1))
    game.board.add_card(PhysicalCard(0, 2))
    game.board.add_card(PhysicalCard(0, 3))
    assert not clue_receiver.is_legal_save_color_clue(clue)


def test_is_legal_save_rank_clue_case_2(game):
    clue_receiver = ClueReceiver(game)
    clue = Clue(
        player_index=0,
        is_color_clue=False,
        value=2,
        card_orders_touched=[0]
    )
    assert clue_receiver.is_legal_save_rank_clue(clue)

    game.board.add_card(PhysicalCard(0, 1))
    game.board.add_card(PhysicalCard(1, 1))
    game.board.add_card(PhysicalCard(2, 1))
    game.board.add_card(PhysicalCard(3, 1))
    game.board.add_card(PhysicalCard(4, 1))

    game.board.add_card(PhysicalCard(0, 2))
    game.board.add_card(PhysicalCard(1, 2))
    game.board.add_card(PhysicalCard(2, 2))
    game.board.add_card(PhysicalCard(3, 2))
    game.board.add_card(PhysicalCard(4, 2))

    assert not clue_receiver.is_legal_save_rank_clue(clue)


def test_is_legal_save_rank_clue_case_1_and_5(game):
    clue_receiver = ClueReceiver(game)
    clue = Clue(
        player_index=0,
        is_color_clue=False,
        value=1,
        card_orders_touched=[0]
    )
    assert not clue_receiver.is_legal_save_rank_clue(clue)

    clue.value = 5
    assert clue_receiver.is_legal_save_rank_clue(clue)


def test_is_legal_save_rank_clue_case_3_or_4(game):
    clue_receiver = ClueReceiver(game)
    clue = Clue(
        player_index=0,
        is_color_clue=False,
        value=3,
        card_orders_touched=[0]
    )
    assert not clue_receiver.is_legal_save_rank_clue(clue)

    game.board.discard_pile.append(Card(1, 0, 3, game.deck))
    assert clue_receiver.is_legal_save_rank_clue(clue)

    game.board.add_card(PhysicalCard(0, 1))
    game.board.add_card(PhysicalCard(0, 2))
    game.board.add_card(PhysicalCard(0, 3))
    assert not clue_receiver.is_legal_save_rank_clue(clue)