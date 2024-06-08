from models.deck import Deck


def test_repartition():
    deck = Deck(suits=[0])
    assert len(deck.cards) == 10
    assert len([card for card in deck.cards if card.rank == 1]) == 3
    assert len([card for card in deck.cards if card.rank == 2]) == 2
    assert len([card for card in deck.cards if card.rank == 3]) == 2
    assert len([card for card in deck.cards if card.rank == 4]) == 2
    assert len([card for card in deck.cards if card.rank == 5]) == 1
