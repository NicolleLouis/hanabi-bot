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
