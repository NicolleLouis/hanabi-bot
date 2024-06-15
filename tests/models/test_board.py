import pytest

from models.board import Board, BoardException
from models.card.physical_card import PhysicalCard


def test_stack_exception():
    board = Board([1])

    with pytest.raises(BoardException):
        board.get_stack(2)


def test_is_card_valid():
    board = Board([1])
    playable_card = PhysicalCard(1, 1)
    unplayable_rank_card = PhysicalCard(1, 2)

    assert board.is_card_valid(playable_card)
    assert not board.is_card_valid(unplayable_rank_card)


def test_add_card():
    board = Board([1])
    card_1 = PhysicalCard(1, 1)
    card_2 = PhysicalCard(1, 2)
    assert not board.is_card_valid(card_2)

    board.add_card(card_1)
    assert board.is_card_valid(card_2)
    assert board.add_card(card_2)


def test_get_playable_rank():
    board = Board([1])
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


def get_playable_suits():
    board = Board([1, 2])
    assert board.get_playable_suits(1) == [1, 2]

    card_1 = PhysicalCard(1, 1)
    card_2 = PhysicalCard(2, 1)

    board.add_card(card_1)
    assert board.get_playable_suits(1) == [2]

    board.add_card(card_2)
    assert board.get_playable_suits(1) is None
