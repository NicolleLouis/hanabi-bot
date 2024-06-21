import pytest

from models.card.physical_card import PhysicalCard, PhysicalCardException


def test_set_suit():
    card = PhysicalCard(-1, -1)
    card.set_suit(1)
    assert card.suit == 1

    with pytest.raises(PhysicalCardException):
        card.set_suit(2)


def test_rank():
    card = PhysicalCard(-1, -1)
    card.set_rank(1)
    assert card.rank == 1

    with pytest.raises(PhysicalCardException):
        card.set_rank(2)
