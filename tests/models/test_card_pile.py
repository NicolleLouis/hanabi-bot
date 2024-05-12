from models.card_pile import CardPile


def test_equality(random_card):
    card = random_card
    pile_1 = CardPile({card})
    pile_2 = CardPile({card})
    assert pile_1 == pile_2


def test_non_equality(random_card_factory):
    card = random_card_factory()
    another_card = random_card_factory()
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
