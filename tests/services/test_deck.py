from models.card.physical_card import PhysicalCard
from models.deck import Deck


def test_remaining_cards(deck_service):
    no_cards = []
    assert len(deck_service.remaining_cards(no_cards)) == 50

    full_deck = Deck(suits=[1, 2, 3, 4, 5]).cards
    assert len(deck_service.remaining_cards(full_deck)) == 0

    card_removed = full_deck.pop()
    assert deck_service.remaining_cards(full_deck) == [card_removed]


def test_is_card_critical(deck_service):
    non_critical_card = PhysicalCard(
        suit=1,
        rank=1
    )
    critical_card = PhysicalCard(
        suit=1,
        rank=5
    )
    assert not deck_service.is_card_critical(non_critical_card, [])
    assert deck_service.is_card_critical(critical_card, [])

    other_non_critical_card = [non_critical_card]
    assert not deck_service.is_card_critical(non_critical_card, other_non_critical_card)

    all_other_non_critical_card = [non_critical_card, non_critical_card]
    assert deck_service.is_card_critical(non_critical_card, all_other_non_critical_card)
