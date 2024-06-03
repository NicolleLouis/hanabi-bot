import pytest

from models.player import Player, PlayerException


def remove_card_with_order(player, order) -> None:
    try:
        for _ in range(len(player.hand)):
            player.remove_card_from_hand(order)
    except PlayerException:
        pass


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
