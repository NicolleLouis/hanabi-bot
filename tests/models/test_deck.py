from constants.color import Color
from models.physical_card import PhysicalCard
from models.deck import Deck


def test_creation():
    deck = Deck()
    assert len(deck.cards) == 50


def test_repartition():
    deck = Deck()
    for color in Color.ALL_COLORS:
        assert deck.cards.number_of_cards_like(PhysicalCard(color, 1)) == 3
        assert deck.cards.number_of_cards_like(PhysicalCard(color, 2)) == 2
        assert deck.cards.number_of_cards_like(PhysicalCard(color, 3)) == 2
        assert deck.cards.number_of_cards_like(PhysicalCard(color, 4)) == 2
        assert deck.cards.number_of_cards_like(PhysicalCard(color, 5)) == 1
