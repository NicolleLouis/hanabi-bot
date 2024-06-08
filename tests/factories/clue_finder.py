import pytest

from services.clue.clue_finder import ClueFinder


@pytest.fixture
def clue_finder(game) -> ClueFinder:
    return ClueFinder(game.player_finder.find_self(), game)
