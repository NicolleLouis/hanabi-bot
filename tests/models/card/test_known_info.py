import pytest

from models.card.known_info import KnownInfo, KnownInfoException
from models.card.physical_card import PhysicalCard


def test_add_positive_clue(card):
    known_info = KnownInfo(card)
    assert not known_info.touched

    known_info.add_positive_clue(is_color_clue=True, value=1)
    assert known_info.positive_suit_clues == [1]
    assert known_info.touched

    known_info.add_positive_clue(is_color_clue=False, value=2)
    assert known_info.positive_rank_clues == [2]


def test_negative_clue(card):
    known_info = KnownInfo(card)
    assert not known_info.touched

    known_info.add_negative_clue(is_color_clue=True, value=1)
    assert known_info.negative_suit_clues == [1]
    assert not known_info.touched

    known_info.add_negative_clue(is_color_clue=False, value=2)
    assert known_info.negative_rank_clues == [2]


def test_sanity_case_success(known_info):
    assert known_info.check_sanity()


def test_sanity_untouched(card):
    known_info = KnownInfo(card)
    known_info.touched = True
    with pytest.raises(KnownInfoException):
        known_info.check_sanity()


def test_sanity_suit_issue(card):
    known_info = KnownInfo(card)
    known_info.positive_suit_clues = [1]
    known_info.negative_suit_clues = [1]
    with pytest.raises(KnownInfoException):
        known_info.check_sanity()


def test_sanity_rank_issue(card):
    known_info = KnownInfo(card)
    known_info.positive_rank_clues = [1]
    known_info.negative_rank_clues = [1]
    with pytest.raises(KnownInfoException):
        known_info.check_sanity()


def test_match_positive_clue(card_factory):
    card_1 = card_factory()
    card_1.known_info.add_positive_clue(is_color_clue=True, value=card_1.suit)
    assert card_1.known_info.match_positive_clue(PhysicalCard(card_1.suit, 1))
    assert not card_1.known_info.match_positive_clue(PhysicalCard(card_1.suit + 1, card_1.rank))

    card_2 = card_factory()
    card_2.known_info.add_positive_clue(is_color_clue=False, value=card_2.rank)
    assert card_2.known_info.match_positive_clue(PhysicalCard(1, card_2.rank))
    assert not card_2.known_info.match_positive_clue(PhysicalCard(card_2.suit, card_2.rank + 1))
