class ColorService:
    COLOR_TRANSLATION = {
        -1: "Unknown",
        0: "Red",
        1: "Yellow",
        2: "Green",
        3: "Blue",
        4: "Purple"
    }

    @classmethod
    def translate_suit(cls, suit: int) -> str:
        return cls.COLOR_TRANSLATION[suit]
