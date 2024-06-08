class PhysicalCard:
    def __init__(
            self,
            suit: int,
            rank: int,
    ):
        self.suit = suit
        self.rank = rank

    def __eq__(self, other):
        return self.suit == other.suit and self.rank == other.rank

    def __hash__(self):
        return hash((self.rank, self.suit))
