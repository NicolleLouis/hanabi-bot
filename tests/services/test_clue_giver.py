from constants.actions import ACTION
from services.clue.clue_giver import ClueGiver


def test_build_color(player, card):
    action = ClueGiver(player, True).build(card)
    assert action.target == player.index
    assert action.action_type == ACTION.COLOR_CLUE
    assert action.value == card.suit


def test_build_rank(player, card):
    action = ClueGiver(player, False).build(card)
    assert action.target == player.index
    assert action.action_type == ACTION.RANK_CLUE
    assert action.value == card.rank


def test_to_card(player, card):
    action = ClueGiver(player, True).to_card(card)
    assert action.value == card.suit


def test_to_slot(player):
    action = ClueGiver(player, True).to_slot(0)
    assert action.value == player.get_card_by_slot(0).suit


def test_to_chop(player):
    action = ClueGiver(player, True).to_chop()
    assert action.value == player.get_chop().suit
