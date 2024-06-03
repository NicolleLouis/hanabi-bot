from models.card import Card


class PlayerException(Exception):
    def __init__(self, message):
        super().__init__(message)


class Player:
    def __init__(self, name, index):
        self.name = name
        self.index = index
        self.hand = []

    def __str__(self):
        return f"{self.name} ({self.index})"

    def remove_card_from_hand(self, card_order):
        card = self.get_card(card_order)
        self.hand.remove(card)
        return card

    def get_card(self, card_order):
        for card in self.hand:
            if card.order == card_order:
                return card
        raise PlayerException(f"Card {card_order} not found in hand")

    def add_card_to_hand(self, card_order, card_rank, card_suit):
        card = Card(
            order=card_order,
            rank=card_rank,
            suit=card_suit,
        )
        self.hand.append(card)
