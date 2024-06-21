import pytest

from models.card.physical_card import PhysicalCard
from models.player import Player, PlayerException


def remove_card_with_order(player, order) -> None:
    hand_size = len(player.hand)
    try:
        for _ in range(hand_size):
            player.remove_card_from_hand(order)
    except PlayerException:
        return


def test_player_str():
    player = Player("Louis", 0)
    assert str(player) == "Louis (0)"


def test_player_initialisation(player):
    assert len(player.hand) == 4


def test_add_card_to_hand(player, card):
    assert len(player.hand) == 4
    player.add_card_to_hand(card_rank=card.rank, card_suit=card.suit, card_order=card.order)
    assert len(player.hand) == 5
    assert player.hand[4].order == card.order
    assert player.hand[4].rank == card.rank
    assert player.hand[4].suit == card.suit
    player.add_card_to_hand(1, 2, 3)
    assert len(player.hand) == 6


def test_get_card(player, card):
    remove_card_with_order(player, card.order)
    player.add_card_to_hand(card_rank=card.rank, card_suit=card.suit, card_order=card.order)
    player_card = player.get_card(card.order)
    assert card == player_card


def test_card_not_found(player):
    remove_card_with_order(player, 0)
    with pytest.raises(PlayerException):
        player.get_card(0)


def test_remove_card(player, card):
    remove_card_with_order(player, card.order)

    player.add_card_to_hand(card_rank=card.rank, card_suit=card.suit, card_order=card.order)
    assert player.get_card(card.order) == card
    card_removed = player.remove_card_from_hand(card.order)
    assert card_removed == card
    with pytest.raises(PlayerException):
        player.get_card(card.order)


def test_remove_card_failure(player, card):
    remove_card_with_order(player, card.order)

    with pytest.raises(PlayerException):
        player.remove_card_from_hand(card.order)


def test_get_chop():
    player = Player("Louis", 0)
    player.add_card_to_hand(0, 1, 1)
    chop_card = player.get_card(0)
    assert player.get_chop() == chop_card

    chop_card.known_info.add_positive_clue(True, 1)
    player.add_card_to_hand(1, 1, 1)
    new_chop_card = player.get_card(1)
    assert player.get_chop() == new_chop_card


def test_get_finesse():
    player = Player("Louis", 0)
    player.add_card_to_hand(0, 1, 1)
    player.add_card_to_hand(1, 1, 1)
    player.add_card_to_hand(2, 1, 1)
    player.add_card_to_hand(3, 1, 1)
    finesse_card = player.get_card(3)
    assert player.get_finesse() == finesse_card

    finesse_card.known_info.add_positive_clue(True, 1)
    new_finesse_card = player.get_card(2)
    assert player.get_finesse() == new_finesse_card


def test_has_physical_card():
    player = Player("Louis", 0)
    player.add_card_to_hand(0, 1, 1)
    player.add_card_to_hand(1, 3, 1)
    player.add_card_to_hand(2, 1, 2)
    player.add_card_to_hand(3, 4, 1)
    player.add_card_to_hand(4, 4, 1)

    assert player.has_physical_card(PhysicalCard(1, 1))
    assert player.has_physical_card(PhysicalCard(1, 4))
    assert not player.has_physical_card(PhysicalCard(1, 0))
