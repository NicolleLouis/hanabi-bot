import pytest

from models.deck import Deck
from services.deck import DeckService


@pytest.fixture
def deck_service() -> DeckService:
    return DeckService(Deck(suits=[1, 2, 3, 4, 5]))
