import random

import pytest

from models.card.card import Card
from models.card.physical_card import PhysicalCard
from models.stack import StackException


def test_valid_card(stack_factory):
    stack = stack_factory()
    while stack.current_rank == 5:
        stack = stack_factory()

    initial_rank = stack.current_rank

    card = Card(
        order=random.randint(0, 50),
        rank=initial_rank + 1,
        suit=stack.suit
    )
    stack.add_card(card)
    assert stack.current_rank == initial_rank + 1


def test_invalid_suit(stack):
    card = Card(
        order=random.randint(0, 50),
        rank=stack.current_rank + 1,
        suit=stack.suit + 1
    )
    with pytest.raises(StackException):
        stack.check_card_validity(card)


def test_invalid_rank(stack):
    card = Card(
        order=random.randint(0, 50),
        rank=stack.current_rank,
        suit=stack.suit
    )
    with pytest.raises(StackException):
        stack.check_card_validity(card)


def test_invalid_card(stack):
    card = Card(
        order=random.randint(0, 50),
        rank=stack.current_rank,
        suit=stack.suit
    )
    initial_rank = stack.current_rank
    stack.add_card(card)
    assert stack.current_rank == initial_rank


def test_get_played_cards(stack):
    stack.current_rank = 0
    assert stack.played_cards == []

    for rank in range(1, 6):
        card = PhysicalCard(stack.suit, rank)
        stack.add_card(card)
        assert len(stack.played_cards) == rank
        assert card in stack.played_cards
