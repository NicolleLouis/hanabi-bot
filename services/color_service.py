class ColorService:
    COLOR_TRANSLATION = {
        0: "red",
        1: "yellow",
        2: "green",
        3: "blue",
        4: "purple"
    }

    @classmethod
    def translate_suit(cls, suit: int) -> str:
        return cls.COLOR_TRANSLATION[suit]
