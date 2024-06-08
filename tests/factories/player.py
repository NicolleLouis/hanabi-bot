import random

import pytest
from faker import Faker

from models.player import Player


@pytest.fixture
def player(card_factory) -> Player:
    fake = Faker()
    name = fake.first_name()
    index = random.randint(0, 4)
    player = Player(name, index)
    for _ in range(4):
        random_card = card_factory()
        player.add_card_to_hand(
            card_order=random_card.order,
            card_suit=random_card.suit,
            card_rank=random_card.rank
        )
    return player


@pytest.fixture
def empty_handed_player() -> Player:
    fake = Faker()
    name = fake.first_name()
    index = random.randint(0, 4)
    return Player(name, index)
