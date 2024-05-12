import pytest

from constants.color import Color
from models.physical_card import PhysicalCard


def test_color_valid(random_physical_card):
    assert random_physical_card.color in Color.ALL_COLORS


def test_str(random_physical_card):
    assert str(random_physical_card) == f"{random_physical_card.color} {random_physical_card.value}"


def test_color_invalid():
    with pytest.raises(ValueError):
        PhysicalCard("Rojo", 1)


def test_value_invalid():
    with pytest.raises(ValueError):
        PhysicalCard(Color.WHITE, 0)
    with pytest.raises(ValueError):
        PhysicalCard(Color.WHITE, 6)


def test_value_valid(random_physical_card):
    assert random_physical_card.value in range(1, 6)
