import random

import pytest

from constants.color import Color
from exceptions.models.card_knowledge import CardKnowledgeException
from models.card_knowledge import CardKnowledge


def test_init():
    card_knowledge = CardKnowledge()
    assert len(card_knowledge.possible_colors) == 5
    assert len(card_knowledge.possible_values) == 5
    assert not card_knowledge.is_known
    assert str(card_knowledge) == 'Unknown: 5 colors possible and 5 potential values'


def test_str_case_known(random_card_knowledge_factory):
    card_knowledge = CardKnowledge()
    card_knowledge.add_positive_color_information(Color.RED)
    card_knowledge.add_positive_value_information(1)

    assert str(card_knowledge) == 'Known: Red 1'


def test_add_positive_card_information(random_card_knowledge_factory):
    card_knowledge = random_card_knowledge_factory()
    while card_knowledge.known_color is not None:
        card_knowledge = random_card_knowledge_factory()  # pragma: no cover

    assert card_knowledge.known_color is None
    assert len(card_knowledge.possible_colors) > 1

    color = random.choice(card_knowledge.possible_colors)
    card_knowledge.add_positive_color_information(color)

    assert len(card_knowledge.possible_colors) == 1
    assert card_knowledge.known_color == color
    assert card_knowledge.possible_colors == [color]


def test_add_positive_value_information(random_card_knowledge_factory):
    card_knowledge = random_card_knowledge_factory()
    while card_knowledge.known_value is not None:
        card_knowledge = random_card_knowledge_factory()  # pragma: no cover

    assert card_knowledge.known_value is None
    assert len(card_knowledge.possible_values) > 1

    value = random.choice(card_knowledge.possible_values)
    card_knowledge.add_positive_value_information(value)

    assert len(card_knowledge.possible_values) == 1
    assert card_knowledge.known_value == value
    assert card_knowledge.possible_values == [value]


def test_add_negative_value_information(random_card_knowledge_factory):
    card_knowledge = random_card_knowledge_factory()
    while card_knowledge.known_value is not None:
        card_knowledge = random_card_knowledge_factory()  # pragma: no cover

    initial_length_possible_value = len(card_knowledge.possible_values)

    assert card_knowledge.known_value is None
    assert initial_length_possible_value > 1

    value = random.choice(card_knowledge.possible_values)
    card_knowledge.add_negative_value_information(value)

    assert len(card_knowledge.possible_values) == initial_length_possible_value - 1
    assert value not in card_knowledge.possible_values


def test_add_negative_color_information(random_card_knowledge_factory):
    card_knowledge = random_card_knowledge_factory()
    while card_knowledge.known_color is not None:
        card_knowledge = random_card_knowledge_factory()  # pragma: no cover

    initial_length_possible_color = len(card_knowledge.possible_colors)

    assert card_knowledge.known_color is None
    assert initial_length_possible_color > 1

    color = random.choice(card_knowledge.possible_colors)
    card_knowledge.add_negative_color_information(color)

    assert len(card_knowledge.possible_colors) == initial_length_possible_color - 1
    assert color not in card_knowledge.possible_colors


def test_clean_case_color(random_card_knowledge_factory):
    card_knowledge = random_card_knowledge_factory()
    while card_knowledge.known_color is not None:
        card_knowledge = random_card_knowledge_factory()  # pragma: no cover

    assert card_knowledge.known_color is None

    color = random.choice(card_knowledge.possible_colors)

    card_knowledge.possible_colors = [color]
    card_knowledge.clean()

    assert card_knowledge.known_color == color


def test_clean_case_value(random_card_knowledge_factory):
    card_knowledge = random_card_knowledge_factory()
    while card_knowledge.known_value is not None:
        card_knowledge = random_card_knowledge_factory()  # pragma: no cover

    assert card_knowledge.known_value is None

    value = random.choice(card_knowledge.possible_values)

    card_knowledge.possible_values = [value]
    card_knowledge.clean()

    assert card_knowledge.known_value == value


def test_clean_case_complete(random_card_knowledge_factory):
    card_knowledge = random_card_knowledge_factory()
    while card_knowledge.is_known is True:
        card_knowledge = random_card_knowledge_factory()  # pragma: no cover

    assert not card_knowledge.is_known

    if card_knowledge.known_color is None:
        color = random.choice(card_knowledge.possible_colors)
        card_knowledge.possible_colors = [color]

    if card_knowledge.known_value is None:
        value = random.choice(card_knowledge.possible_values)
        card_knowledge.possible_values = [value]

    card_knowledge.clean()

    assert card_knowledge.is_known


def test_add_incoherent_color_positive_information():
    card_knowledge = CardKnowledge()
    card_knowledge.add_positive_color_information(Color.RED)

    with pytest.raises(CardKnowledgeException):
        card_knowledge.add_positive_color_information(Color.WHITE)


def test_add_incoherent_value_positive_information():
    card_knowledge = CardKnowledge()
    card_knowledge.add_positive_value_information(1)

    with pytest.raises(CardKnowledgeException):
        card_knowledge.add_positive_value_information(2)


def test_add_incoherent_value_negative_information():
    card_knowledge = CardKnowledge()
    card_knowledge.add_positive_value_information(1)

    with pytest.raises(CardKnowledgeException):
        card_knowledge.add_negative_value_information(1)


def test_add_incoherent_color_negative_information():
    card_knowledge = CardKnowledge()
    card_knowledge.add_positive_color_information(Color.WHITE)

    with pytest.raises(CardKnowledgeException):
        card_knowledge.add_negative_color_information(Color.WHITE)
