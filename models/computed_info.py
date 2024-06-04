class ComputedInfo:
    def __init__(self):
        self.touched = False
        self.playable = False
        self.estimated_rank = None
        self.estimated_suit = None

    def pretty_print(self):
        print("Computed Info:")
