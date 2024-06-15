from models.card.card import Card
from models.card.physical_card import PhysicalCard
from services.card import CardService


def test_convert_to_physical_cards():
    mixed_cards = [
        Card(order=0, suit=0, rank=0),
        PhysicalCard(suit=0, rank=1),
    ]
    physical_cards = CardService.convert_to_physical_cards(mixed_cards)
    for card in physical_cards:
        assert isinstance(card, PhysicalCard)
