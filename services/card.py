from models.card.card import Card
from models.card.physical_card import PhysicalCard


class CardServiceException(Exception):
    pass


class CardService:
    @staticmethod
    def convert_to_physical_cards(cards):
        physical_cards = []
        for card in cards:
            if isinstance(card, Card):
                physical_cards.append(card.physical_card)
            elif isinstance(card, PhysicalCard):
                physical_cards.append(card)
            else:
                raise CardServiceException("Unrecognized card type")
        return physical_cards
