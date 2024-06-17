import pytest

from constants.actions import ACTION
from models.action import ActionException, Action
from models.card.card import Card
from models.clue import Clue


def test_to_clue_case_error(game):
    with pytest.raises(ActionException):
        action = Action(ACTION.PLAY, 0)
        action.to_clue(game)


def test_to_clue_case_color_clue(game):
    action = Action(ACTION.COLOR_CLUE, 1, value=1)
    clue = action.to_clue(game)
    assert clue.player_index == 1
    assert clue.value == 1
    assert clue.is_color_clue

    player = game.player_finder.get_player(1)
    player.hand = [
        Card(0, 1, 2),
        Card(1, 2, 1),
        Card(2, 3, 3),
    ]
    clue = action.to_clue(game)
    assert clue.card_orders_touched == [0]


def test_to_clue_case_rank_clue(game):
    action = Action(ACTION.RANK_CLUE, 1, value=1)
    clue = action.to_clue(game)
    assert isinstance(clue, Clue)
    assert clue.player_index == 1
    assert clue.value == 1
    assert not clue.is_color_clue

    player = game.player_finder.get_player(1)
    player.hand = [
        Card(0, 1, 2),
        Card(1, 2, 1),
        Card(2, 3, 1),
    ]
    clue = action.to_clue(game)
    assert clue.card_orders_touched == [1, 2]
