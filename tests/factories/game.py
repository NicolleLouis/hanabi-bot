import random

import pytest
from faker import Faker

from models.game import Game


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
