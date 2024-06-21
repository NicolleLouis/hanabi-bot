import pytest

from models.board import Board, BoardException
from models.card.card import Card
from models.card.physical_card import PhysicalCard
from models.deck import Deck


def test_stack_exception(game):
    board = Board(game, [1])

    with pytest.raises(BoardException):
        board.get_stack(2)


def test_is_card_valid(game):
    board = Board(game, [1])
    playable_card = PhysicalCard(1, 1)
    unplayable_rank_card = PhysicalCard(1, 2)

    assert board.is_card_valid(playable_card)
    assert not board.is_card_valid(unplayable_rank_card)


def test_add_card(game):
    board = Board(game, [1])
    card_1 = PhysicalCard(1, 1)
    card_2 = PhysicalCard(1, 2)
    assert not board.is_card_valid(card_2)

    board.add_card(card_1)
    assert board.is_card_valid(card_2)
    assert board.add_card(card_2)


def test_get_playable_rank(game):
    board = Board(game, [1])
    assert board.get_playable_rank(1) == 1

    card_1 = PhysicalCard(1, 1)
    card_2 = PhysicalCard(1, 2)
    card_3 = PhysicalCard(1, 3)
    card_4 = PhysicalCard(1, 4)
    card_5 = PhysicalCard(1, 5)

    board.add_card(card_1)
    assert board.get_playable_rank(1) == 2

    board.add_card(card_2)
    assert board.get_playable_rank(1) == 3

    board.add_card(card_3)
    assert board.get_playable_rank(1) == 4

    board.add_card(card_4)
    assert board.get_playable_rank(1) == 5

    board.add_card(card_5)
    assert board.get_playable_rank(1) is None


def test_get_playable_suits(game):
    board = Board(game, [1, 2])
    assert board.get_playable_suits(1) == [1, 2]

    card_1 = PhysicalCard(1, 1)
    card_2 = PhysicalCard(2, 1)

    board.add_card(card_1)
    assert board.get_playable_suits(1) == [2]

    board.add_card(card_2)
    assert board.get_playable_suits(1) == []


def test_is_critical(game):
    board = Board(game, [0])

    card_1 = PhysicalCard(0, 1)
    assert not board.is_critical(card_1)

    board.discard_pile.append(Card(0, 0, 1, board.deck))
    board.discard_pile.append(Card(0, 0, 1, board.deck))
    assert board.is_critical(card_1)

    card_2 = PhysicalCard(0, 5)
    assert board.is_critical(card_2)


def test_get_playable_suits_prompt_case(game):
    board = Board(game, [1, 2])
    assert board.get_playable_suits(1) == [1, 2]

    other_player = game.brain.other_players()[0]
    other_player.add_card_to_hand(0, 1, 2, Deck([1, 2]))
    card = other_player.get_card(0)
    card.computed_info.touched = True

    assert board.get_playable_suits(2) == [2]
    assert board.get_playable_suits(1) == [1]


def test_get_playable_rank_prompt_case(game):
    board = Board(game, [1, 2])
    assert board.get_playable_rank(2) == 1
    assert board.get_playable_rank(1) == 1

    other_player = game.brain.other_players()[0]
    other_player.add_card_to_hand(0, 1, 2, Deck([1, 2]))
    card = other_player.get_card(0)
    card.computed_info.touched = True

    assert board.get_playable_rank(2) == 2
    assert board.get_playable_rank(1) == 1


def test_get_missing_card_before_play(game):
    board = Board(game, [1])
    card = PhysicalCard(1, 3)
    missing_cards = board.get_missing_card_before_play(card)
    assert len(missing_cards) == 2
    assert PhysicalCard(1, 1) in missing_cards
    assert PhysicalCard(1, 2) in missing_cards
    assert PhysicalCard(1, 3) not in missing_cards
    assert PhysicalCard(1, 4) not in missing_cards
    assert PhysicalCard(1, 5) not in missing_cards

    stack = board.get_stack(1)
    stack.current_rank = 2
    card = PhysicalCard(1, 5)
    missing_cards = board.get_missing_card_before_play(card)
    assert len(missing_cards) == 2
    for rank in range(3, 5):
        assert PhysicalCard(1, rank) in missing_cards
    assert PhysicalCard(1, 1) not in missing_cards
    assert PhysicalCard(1, 2) not in missing_cards
    assert PhysicalCard(1, 5) not in missing_cards
