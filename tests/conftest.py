import random

import pytest

from constants.color import Color
from models.card_knowledge import CardKnowledge
from models.physical_card import PhysicalCard
from models.card_pile import CardPile


@pytest.fixture
def random_physical_card():
    color = random.choice(Color.ALL_COLORS)
    number = random.randint(1, 5)
    yield PhysicalCard(color, number)


@pytest.fixture
def random_physical_card_factory():
    def _random_physical_card():
        color = random.choice(Color.ALL_COLORS)
        number = random.randint(1, 5)
        return PhysicalCard(color, number)
    return _random_physical_card


@pytest.fixture
def random_card_knowledge_factory():
    def _random_card_knowledge():
        card_knowledge = CardKnowledge()
        for _ in range(random.randint(1, 4)):
            card_knowledge.add_negative_color_information(random.choice(card_knowledge.possible_colors))
        for _ in range(random.randint(1, 4)):
            card_knowledge.add_negative_value_information(random.choice(card_knowledge.possible_values))
        return card_knowledge
    return _random_card_knowledge


@pytest.fixture
def random_card_pile(random_physical_card):
    card_pile = {random_physical_card for _ in range(random.randint(1, 10))}
    yield CardPile(card_pile)


@pytest.fixture
def random_card_pile_factory(random_physical_card_factory):
    def _random_card_pile():
        card_pile = {random_physical_card_factory() for _ in range(random.randint(1, 10))}
        return CardPile(card_pile)

    return _random_card_pile
