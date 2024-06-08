import random
import pytest

from models.card.card import Card


@pytest.fixture
def card():
    suit = random.randint(1, 5)
    number = random.randint(1, 5)
    order = random.randint(0, 50)
    yield Card(order, suit, number)


@pytest.fixture
def card_factory():
    def _card():
        suit = random.randint(1, 5)
        number = random.randint(1, 5)
        order = random.randint(0, 50)
        return Card(order, suit, number)

    return _card
