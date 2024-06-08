from models.card.physical_card import PhysicalCard


class Deck:
    def __init__(self, suits):
        self.cards = []
        for suit in suits:
            self.fill_suit(suit)

    def fill_suit(self, suit):
        rank_repartition = {
            1: 3,
            2: 2,
            3: 2,
            4: 2,
            5: 1
        }
        for rank, quantity in rank_repartition.items():
            for _ in range(quantity):
                self.cards.append(PhysicalCard(
                    rank=rank,
                    suit=suit
                ))
