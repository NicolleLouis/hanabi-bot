from unittest.mock import patch

from models.board import Board
from models.card.card import Card
from models.card.computed_info import ComputedInfo
from models.card.physical_card import PhysicalCard
from models.deck import Deck


def test_card_str():
    card = Card(
        order=0,
        suit=0,
        rank=0,
    )
    assert str(card) == "Red 0"


def test_update_playability_case_unknown_yet(game):
    with patch.object(ComputedInfo, 'update_playability') as mock_update_playability:
        card = Card(
            order=0,
            suit=0,
            rank=1,
        )
        board = Board(game, [0])
        card.update_playability(board)
        assert card.is_known
        mock_update_playability.assert_not_called()


def test_update_playability_case_unknown(game):
    with patch.object(ComputedInfo, 'update_playability') as mock_update_playability:
        card = Card(
            order=0,
            suit=-1,
            rank=1,
        )
        board = Board(game, [0])
        card.update_playability(board)
        assert not card.is_known
        mock_update_playability.assert_called_once()


def test_update_playability_case_known(game):
    with patch.object(ComputedInfo, 'update_playability') as mock_update_playability:
        card = Card(
            order=0,
            suit=0,
            rank=1,
        )
        board = Board(game, [0])
        card.set_known(0, 1)
        card.update_playability(board)
        mock_update_playability.assert_not_called()
        assert card.playable

        board.add_card(PhysicalCard(suit=0, rank=1))
        card.update_playability(board)
        assert not card.playable


def test_set_known():
    card = Card(
        order=0,
        suit=0,
        rank=1,
    )
    card.set_known(0, 1)
    assert card.is_known
    assert card.suit == 0
    assert card.rank == 1


def test_set_playable():
    card = Card(
        order=0,
        suit=0,
        rank=1,
    )
    card.set_playable(True)
    assert card.playable
    card.set_playable(False)
    assert not card.playable


def test_set_among_possibilities():
    card = Card(
        order=0,
        suit=0,
        rank=1,
        deck=Deck([0])
    )
    assert len(card.computed_info.possible_cards) == 5

    card.set_among_possibilities([PhysicalCard(suit=0, rank=1)])
    assert len(card.computed_info.possible_cards) == 1
    assert PhysicalCard(suit=0, rank=1) in card.computed_info.possible_cards
