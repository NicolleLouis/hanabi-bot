import pytest

from constants.color import Color
from models.card import Card


def test_color_valid(random_card):
    assert random_card.color in Color.ALL_COLORS


def test_color_invalid():
    with pytest.raises(ValueError):
        Card("Rojo", 1)


def test_value_invalid():
    with pytest.raises(ValueError):
        Card(Color.WHITE, 0)
    with pytest.raises(ValueError):
        Card(Color.WHITE, 6)


def test_value_valid(random_card):
    assert random_card.value in range(1, 6)
