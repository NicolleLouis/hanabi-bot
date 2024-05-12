import random
import uuid

from constants.color import Color
from models.physical_card import PhysicalCard
from models.card_pile import CardPile


def test_equality(random_physical_card):
    card = random_physical_card
    pile_1 = CardPile({card})
    pile_2 = CardPile({card})
    assert pile_1 == pile_2


def test_hash_uuid(random_card_pile):
    card_pile = random_card_pile
    assert isinstance(card_pile.id, uuid.UUID)


def test_hash_collision_resistance(random_card_pile_factory):
    hash_values = [hash(random_card_pile_factory()) for _ in range(1000)]
    assert len(hash_values) == len(set(hash_values))


def test_non_equality(random_physical_card_factory):
    card = random_physical_card_factory()
    another_card = random_physical_card_factory()
    pile_1 = CardPile({card})
    pile_2 = CardPile({another_card})
    assert pile_1 != pile_2


def test_str_card_pile():
    card_pile = CardPile()
    assert str(card_pile) == "0 cards in pile"


def test_length(random_card_pile):
    assert len(random_card_pile) == len(random_card_pile.cards)


def test_addition(random_card_pile_factory):
    card_pile = random_card_pile_factory()
    card_pile_2 = random_card_pile_factory()
    new_pile = card_pile + card_pile_2
    assert len(new_pile) == len(card_pile) + len(card_pile_2)


def test_subtraction_complete_case(random_card_pile):
    card_pile = random_card_pile
    card_pile_2 = CardPile(card_pile.cards)
    new_pile = card_pile_2 - card_pile
    assert new_pile == CardPile()


def test_subtraction_with_non_existing_cards(random_card_pile):
    card_pile = CardPile()
    card_pile_2 = random_card_pile
    new_pile = card_pile - card_pile_2
    assert len(new_pile) == 0


def test_subtraction_with_remaining_cards(random_card_pile_factory):
    card_pile = random_card_pile_factory()
    card_pile_2 = random_card_pile_factory()
    new_pile = card_pile + card_pile_2
    new_pile_2 = new_pile - card_pile
    assert new_pile_2 == card_pile_2


def test_draw_cards(random_card_pile):
    card_pile = random_card_pile
    pile_size = len(card_pile)
    hand = card_pile.draw_cards(pile_size - 1)
    assert len(hand) == pile_size - 1
    assert len(card_pile) == 1


def test_draw_too_many_cards(random_card_pile):
    card_pile = random_card_pile
    pile_size = len(card_pile)
    hand = card_pile.draw_cards(pile_size + 1)
    assert len(hand) == pile_size
    assert len(card_pile) == 0


def test_pick_cards(random_card_pile):
    card_pile = random_card_pile
    pile_size = len(card_pile)
    card_taken = card_pile.pick_cards(1)
    assert len(card_taken) == 1

    # Should not take card away from base pile
    assert len(card_pile) == pile_size


def test_pick_too_many_cards(random_card_pile):
    card_pile = random_card_pile
    pile_size = len(card_pile)
    card_taken = card_pile.pick_cards(pile_size + 1)
    assert len(card_taken) == pile_size
    assert len(card_pile) == pile_size


def test_add_card(random_card_pile, random_physical_card_factory):
    card_pile = random_card_pile
    initial_size = len(card_pile)
    card = random_physical_card_factory()
    card_pile.add_card(card)
    assert card in card_pile.cards
    assert len(card_pile) == initial_size + 1


def test_is_empty(random_card_pile):
    card_pile = random_card_pile
    assert not card_pile.is_empty()
    card_pile.draw_cards(len(card_pile))
    assert card_pile.is_empty()


def test_has_card_equivalent(random_card_pile, random_physical_card_factory):
    card_pile = random_card_pile
    card = random_physical_card_factory()
    while card_pile.has_card_equivalent(card):
        card = random_physical_card_factory()  # pragma: no cover

    assert not card_pile.has_card_equivalent(card)

    card_pile.add_card(card)
    assert card_pile.has_card_equivalent(card)


def test_number_of_cards_like(random_card_pile, random_physical_card):
    card = random_physical_card
    card_pile = random_card_pile
    card_already_present = card_pile.number_of_cards_like(card)

    duplicate_number = random.randint(1, 10)
    for _ in range(duplicate_number):
        card_pile.add_card(PhysicalCard(color=card.color, value=card.value))
    assert card_pile.number_of_cards_like(card) == duplicate_number + card_already_present


def test_pretty_print(capfd):
    card_pile = CardPile({PhysicalCard(Color.GREEN, 2)})
    card_pile.pretty_print()
    out, err = capfd.readouterr()

    assert out == 'Green 2\n'
