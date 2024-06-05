from constants.actions import ACTION
from services.clue_giver import ClueGiver


def test_build_color(player, card):
    body = ClueGiver(player, True).build(card)
    assert body["target"] == player.index
    assert body["type"] == ACTION.COLOR_CLUE
    assert body["value"] == card.suit


def test_build_rank(player, card):
    body = ClueGiver(player, False).build(card)
    assert body["target"] == player.index
    assert body["type"] == ACTION.RANK_CLUE
    assert body["value"] == card.rank


def test_to_card(player, card):
    body = ClueGiver(player, True).to_card(card)
    assert body["value"] == card.suit


def test_to_slot(player):
    body = ClueGiver(player, True).to_slot(0)
    assert body["value"] == player.get_card_by_slot(0).suit


def test_to_chop(player):
    body = ClueGiver(player, True).to_chop()
    assert body["value"] == player.get_chop().suit
