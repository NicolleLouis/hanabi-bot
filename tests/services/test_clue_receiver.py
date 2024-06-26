from unittest.mock import patch

import pytest

from models.card.card import Card
from models.card.physical_card import PhysicalCard
from models.clue import Clue
from services.card import CardService
from services.clue.clue_receiver import ClueReceiver, ClueReceiverException


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
    player = game.player_finder.find_self()
    clue = Clue(
        player_index=player.index,
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
    player = game.player_finder.find_self()
    clue = Clue(
        player_index=player.index,
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


def test_clue_giver(game):
    clue_receiver = ClueReceiver(game)
    game.current_player_index = 0
    expected_player = game.player_finder.get_player(0)
    assert expected_player == clue_receiver.clue_giver()


def test_clue_receiver(game):
    clue_receiver = ClueReceiver(game)
    clue = Clue(
        player_index=0,
        is_color_clue=True,
        value=0,
        card_orders_touched=[0]
    )
    expected_player = game.player_finder.get_player(0)
    assert expected_player == clue_receiver.clue_receiver(clue)


def test_promise_playable_card_in_hand(game):
    clue_receiver = ClueReceiver(game)
    # Player Hand is R2, R3, R4, R5, R1
    player = game.player_finder.find_self()
    player.add_card_to_hand(0, -1, -1, game.deck)
    player.add_card_to_hand(1, -1, -1, game.deck)
    player.add_card_to_hand(2, -1, -1, game.deck)
    player.add_card_to_hand(3, -1, -1, game.deck)
    player.add_card_to_hand(4, -1, -1, game.deck)

    # No cards touched so promise is impossible (until finesse)
    with pytest.raises(ClueReceiverException):
        clue_receiver.promise_playable_card_in_hand(PhysicalCard(0, 1))

    # Touch all cards with a red clue
    clue_receiver.receive_clue(Clue(
        player_index=player.index,
        is_color_clue=True,
        value=0,
        card_orders_touched=[0, 1, 2, 3, 4]
    ))
    chop = player.get_card_by_slot(5)
    assert chop.is_known
    assert chop.rank == 1

    # Promise a already clued card so no more promises
    clue_receiver.promise_playable_card_in_hand(PhysicalCard(0, 1))
    slot_1 = player.get_card_by_slot(1)
    assert not slot_1.is_known
    assert slot_1.rank == -1

    # Promise a card that is not in hand yet
    clue_receiver.promise_playable_card_in_hand(PhysicalCard(0, 2))
    assert slot_1.is_known
    assert slot_1.rank == 2


def test_compute_own_hand_consequences(game):
    clue_receiver = ClueReceiver(game)
    player = game.player_finder.find_self()
    other_player = game.brain.other_players()[0]
    other_player.add_card_to_hand(0, -1, -1, game.deck)
    clue = Clue(
            player_index=other_player.index,
            is_color_clue=True,
            value=2,
            card_orders_touched=[0]
        )
    clued_card = other_player.get_card(0)

    # Card is not known so it should raise an exception
    with pytest.raises(ClueReceiverException):
        clue_receiver.compute_own_hand_consequences(clued_card, clue)

    clued_card.set_known(suit=0, rank=2)
    # No legal target in player hand
    with pytest.raises(ClueReceiverException):
        clue_receiver.compute_own_hand_consequences(clued_card, clue)

    player.add_card_to_hand(1, -1, -1, game.deck)
    card = player.get_card(1)
    card.set_touched(True)
    card.known_info.add_positive_clue(True, 0)
    clue_receiver.compute_own_hand_consequences(clued_card, clue)
    assert card.is_known
    assert card.suit == 0
    assert card.rank == 1
    assert card.playable
