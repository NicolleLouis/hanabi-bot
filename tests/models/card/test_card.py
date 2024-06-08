from models.card.card import Card


def test_card_str():
    card = Card(
        order=0,
        suit=0,
        rank=0,
    )
    assert str(card) == "0 of 0"
