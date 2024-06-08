from models.board import Board
from models.card.card import Card
from models.card.physical_card import PhysicalCard
from models.deck import Deck


def test_initialization():
    deck = Deck([1, 2, 3, 4, 5])
    card = Card(
        order=0,
        rank=1,
        suit=1,
        deck=deck
    )
    assert card.computed_info.possible_cards == set(deck.cards)


def test_remove_possibility():
    deck = Deck([1])
    card = Card(
        order=0,
        rank=1,
        suit=1,
        deck=deck
    )
    card.computed_info.remove_possibility(PhysicalCard(1, 2))
    assert len(card.computed_info.possible_cards) == 4
    assert (PhysicalCard(1, 1)) in card.computed_info.possible_cards
    assert (PhysicalCard(1, 2)) not in card.computed_info.possible_cards


def test_negative_rank_clues():
    deck = Deck([1])
    card = Card(
        order=0,
        rank=1,
        suit=1,
        deck=deck
    )
    card.known_info.add_negative_clue(is_color_clue=False, value=2)
    assert len(card.computed_info.possible_cards) == 4
    assert (PhysicalCard(1, 2)) not in card.computed_info.possible_cards


def test_negative_suit_clues():
    deck = Deck([1, 2])
    card = Card(
        order=0,
        rank=1,
        suit=1,
        deck=deck
    )
    card.known_info.add_negative_clue(is_color_clue=True, value=2)
    assert len(card.computed_info.possible_cards) == 5
    assert (PhysicalCard(2, 1)) not in card.computed_info.possible_cards
    assert (PhysicalCard(2, 2)) not in card.computed_info.possible_cards
    assert (PhysicalCard(2, 3)) not in card.computed_info.possible_cards
    assert (PhysicalCard(2, 4)) not in card.computed_info.possible_cards
    assert (PhysicalCard(2, 5)) not in card.computed_info.possible_cards


def test_positive_suit_clues():
    deck = Deck([1, 2])
    card = Card(
        order=0,
        rank=1,
        suit=1,
        deck=deck
    )
    card.known_info.add_positive_clue(is_color_clue=True, value=1)
    assert len(card.computed_info.possible_cards) == 5
    assert (PhysicalCard(2, 1)) not in card.computed_info.possible_cards
    assert (PhysicalCard(2, 2)) not in card.computed_info.possible_cards
    assert (PhysicalCard(2, 3)) not in card.computed_info.possible_cards
    assert (PhysicalCard(2, 4)) not in card.computed_info.possible_cards
    assert (PhysicalCard(2, 5)) not in card.computed_info.possible_cards


def test_positive_rank_clues():
    deck = Deck([1, 2, 3, 4, 5])
    card = Card(
        order=0,
        rank=1,
        suit=1,
        deck=deck
    )
    card.known_info.add_positive_clue(is_color_clue=False, value=1)
    assert len(card.computed_info.possible_cards) == 5
    assert (PhysicalCard(1, 1)) in card.computed_info.possible_cards
    assert (PhysicalCard(2, 1)) in card.computed_info.possible_cards
    assert (PhysicalCard(3, 1)) in card.computed_info.possible_cards
    assert (PhysicalCard(4, 1)) in card.computed_info.possible_cards
    assert (PhysicalCard(5, 1)) in card.computed_info.possible_cards


def test_update_playability():
    board = Board([1, 2])
    card = Card(0, -1, -1)
    card.computed_info.possible_cards = {PhysicalCard(1, 1), PhysicalCard(2, 2)}

    card.computed_info.update_playability(board)
    assert not card.playable
    board.add_card(PhysicalCard(2, 1))

    card.computed_info.update_playability(board)
    assert card.playable
