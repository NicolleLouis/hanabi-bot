import random

import pytest

from constants.color import Color
from models.card import Card
from models.card_pile import CardPile


@pytest.fixture
def random_card():
    color = random.choice(Color.ALL_COLORS)
    number = random.randint(1, 5)
    yield Card(color, number)


@pytest.fixture
def random_card_factory():
    def _random_card():
        color = random.choice(Color.ALL_COLORS)
        number = random.randint(1, 5)
        return Card(color, number)
    return _random_card


@pytest.fixture
def random_card_pile(random_card):
    card_pile = {random_card for _ in range(random.randint(1, 10))}
    yield CardPile(card_pile)


@pytest.fixture
def random_card_pile_factory(random_card_factory):
    def _random_card_pile():
        card_pile = {random_card_factory() for _ in range(random.randint(1, 10))}
        return CardPile(card_pile)
    return _random_card_pile
