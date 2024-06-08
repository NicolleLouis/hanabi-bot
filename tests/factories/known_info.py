import random

import pytest

from models.card.known_info import KnownInfo


def random_clue_value():
    return random.randint(1, 5)


def random_clue_number():
    return random.randint(0, 4)


@pytest.fixture
def known_info(card) -> KnownInfo:
    known_info = KnownInfo(card)
    if random.choice([True, False]):
        known_info.add_positive_clue(is_color_clue=True, value=random_clue_value())

    if random.choice([True, False]):
        known_info.add_positive_clue(is_color_clue=True, value=random_clue_value())

    negative_rank_clue_number = random_clue_number()
    negative_color_clue_number = random_clue_number()

    for _ in range(negative_rank_clue_number):
        clue_value = random_clue_value()
        if clue_value not in known_info.positive_rank_clues:
            known_info.add_negative_clue(is_color_clue=False, value=clue_value)

    for _ in range(negative_color_clue_number):
        clue_value = random_clue_value()
        if clue_value not in known_info.positive_suit_clues:
            known_info.add_negative_clue(is_color_clue=True, value=clue_value)

    return known_info
