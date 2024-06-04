from models.card import Card


def test_card_str():
    card = Card(
        order=0,
        suit=0,
        rank=0,
    )
    assert str(card) == "0 of 0"


def test_equivalent():
    card_1 = Card(
        order=0,
        suit=0,
        rank=0,
    )
    card_2 = Card(
        order=1,
        suit=0,
        rank=0,
    )
    assert card_1.equivalent(card_2)
