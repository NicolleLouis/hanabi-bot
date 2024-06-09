import pytest

from models.card.card import Card
from models.clue import Clue
from services.clue.clue_finder import ClueFinderException


def test_other_players(clue_finder):
    other_players = clue_finder.other_players()
    assert clue_finder.player not in other_players
    assert len(other_players) == len(clue_finder.game.players) - 1


def test_playable_cards(clue_finder):
    other_player = clue_finder.other_players()[0]
    other_player.add_card_to_hand(0, 1, 1)
    playable_card = other_player.get_card(0)
    other_player.add_card_to_hand(1, 4, 4)
    non_playable_card = other_player.get_card(1)

    assert playable_card in clue_finder.playable_cards()
    assert non_playable_card not in clue_finder.playable_cards()


def test_is_card_color_focusable(clue_finder):
    other_player = clue_finder.other_players()[0]
    other_player.add_card_to_hand(0, 1, 1)
    focusable_card = other_player.get_card(0)
    other_player.add_card_to_hand(1, 4, 1)
    non_focusable_card = other_player.get_card(1)

    assert clue_finder.is_card_color_focusable(focusable_card)
    assert not clue_finder.is_card_color_focusable(non_focusable_card)


def test_is_card_rank_focusable(clue_finder):
    other_player = clue_finder.other_players()[0]
    other_player.add_card_to_hand(0, 1, 1)
    focusable_card = other_player.get_card(0)
    other_player.add_card_to_hand(1, 1, 4)
    non_focusable_card = other_player.get_card(1)

    assert clue_finder.is_card_rank_focusable(focusable_card)
    assert not clue_finder.is_card_rank_focusable(non_focusable_card)


def test_filter_touchable_cards(clue_finder):
    other_player = clue_finder.other_players()[0]
    other_player.add_card_to_hand(0, 1, 1)
    focusable_card = other_player.get_card(0)
    other_player.add_card_to_hand(1, 1, 1)
    non_focusable_card = other_player.get_card(1)

    assert focusable_card in clue_finder.filter_touchable_cards(other_player.hand)
    assert non_focusable_card not in clue_finder.filter_touchable_cards(other_player.hand)


def test_find_play_clue_case_1(clue_finder):
    other_player = clue_finder.other_players()[0]
    other_player.add_card_to_hand(0, 1, 1)
    other_player.add_card_to_hand(1, 1, 1)
    expected_clues = [
        Clue(
            player_index=other_player.index,
            is_color_clue=True,
            value=1,
            card_orders_touched=[0, 1],
        ),
        Clue(
            player_index=other_player.index,
            is_color_clue=False,
            value=1,
            card_orders_touched=[0, 1],
        )
    ]
    real_clues = clue_finder.find_play_clues()
    for clue in real_clues:
        assert clue in expected_clues
    assert len(real_clues) == len(expected_clues)


def test_find_play_clue_case_2(clue_finder):
    other_player = clue_finder.other_players()[0]
    other_player.add_card_to_hand(0, 5, 1)
    other_player.add_card_to_hand(1, 1, 1)
    other_player.add_card_to_hand(2, 2, 2)
    expected_clues = [
        Clue(
            player_index=other_player.index,
            is_color_clue=False,
            value=1,
            card_orders_touched=[1],
        )
    ]
    real_clues = clue_finder.find_play_clues()
    for clue in real_clues:
        assert clue in expected_clues
    assert len(real_clues) == len(expected_clues)


def test_generate_clue_error_case(clue_finder):
    fake_card = Card(420, 1, 1)

    with pytest.raises(ClueFinderException):
        clue_finder.generate_clue(fake_card, True)
