from services.color_service import ColorService


class PhysicalCardException(Exception):
    pass


class PhysicalCard:
    def __init__(
            self,
            suit: int,
            rank: int,
    ):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        color = ColorService.translate_suit(self.suit)
        return f"{color} {self.rank}"

    def __eq__(self, other):
        return self.suit == other.suit and self.rank == other.rank

    def __hash__(self):
        return hash((self.rank, self.suit))

    def is_known(self):
        return self.suit != -1 and self.rank != -1

    def set_suit(self, suit):
        if self.suit not in [-1, suit]:
            raise PhysicalCardException("Suit already set and incompatible")
        self.suit = suit

    def set_rank(self, rank):
        if self.rank not in [-1, rank]:
            raise PhysicalCardException("Rank already set and incompatible")
        self.rank = rank
