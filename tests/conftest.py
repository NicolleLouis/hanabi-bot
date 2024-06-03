import random

import pytest
from faker import Faker

from models.card import Card
from models.client import Client
from models.game import Game
from models.player import Player


@pytest.fixture
def card():
    suit = random.randint(1, 5)
    number = random.randint(1, 5)
    order = random.randint(0, 50)
    yield Card(order, suit, number)


@pytest.fixture
def card_factory():
    def _card():
        suit = random.randint(1, 5)
        number = random.randint(1, 5)
        order = random.randint(0, 50)
        return Card(order, suit, number)

    return _card


@pytest.fixture
def client() -> Client:
    return Client("None", "None")


@pytest.fixture
def game(client) -> Game:
    game = Game(client)
    player_number = random.randint(2, 5)
    fake = Faker()

    player_names = [fake.first_name() for _ in range(player_number)]
    own_index = random.randint(0, player_number - 1)
    table_id = fake.word()
    data = {
        "playerNames": player_names,
        "ourPlayerIndex": own_index,
        "tableID": table_id
    }

    game.start(data)
    return game


@pytest.fixture
def player(card_factory) -> Player:
    fake = Faker()
    name = fake.first_name()
    index = random.randint(0, 4)
    player = Player(name, index)
    for _ in range(4):
        card = card_factory()
        player.add_card_to_hand(
            card_order=card.order,
            card_suit=card.suit,
            card_rank=card.rank
        )
    return player
