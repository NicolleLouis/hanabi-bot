import pytest

from models.known_info import KnownInfo, KnownInfoException


def test_add_positive_clue():
    known_info = KnownInfo()
    assert not known_info.touched

    known_info.add_positive_clue(is_color_clue=True, value=1)
    assert known_info.positive_suit_clues == [1]
    assert known_info.touched

    known_info.add_positive_clue(is_color_clue=False, value=2)
    assert known_info.positive_rank_clues == [2]


def test_negative_clue():
    known_info = KnownInfo()
    assert not known_info.touched

    known_info.add_negative_clue(is_color_clue=True, value=1)
    assert known_info.negative_suit_clues == [1]
    assert not known_info.touched

    known_info.add_negative_clue(is_color_clue=False, value=2)
    assert known_info.negative_rank_clues == [2]


def test_sanity_case_success(known_info):
    assert known_info.check_sanity()


def test_sanity_untouched():
    known_info = KnownInfo()
    known_info.touched = True
    with pytest.raises(KnownInfoException):
        known_info.check_sanity()


def test_sanity_suit_issue():
    known_info = KnownInfo()
    known_info.positive_suit_clues = [1]
    known_info.negative_suit_clues = [1]
    with pytest.raises(KnownInfoException):
        known_info.check_sanity()


def test_sanity_rank_issue():
    known_info = KnownInfo()
    known_info.positive_rank_clues = [1]
    known_info.negative_rank_clues = [1]
    with pytest.raises(KnownInfoException):
        known_info.check_sanity()
