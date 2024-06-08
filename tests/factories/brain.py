import pytest

from models.brain import Brain


@pytest.fixture
def brain(game) -> Brain:
    brain = Brain(game)
    brain.set_player(game.player_finder.find_self())
    return brain
