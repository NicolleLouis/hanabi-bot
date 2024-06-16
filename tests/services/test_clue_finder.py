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
    other_player.add_card_to_hand(1, 1, 2)
    expected_clues = [
        Clue(
            player_index=other_player.index,
            is_color_clue=False,
            value=1,
            card_orders_touched=[0, 1],
        ),
        Clue(
            player_index=other_player.index,
            is_color_clue=True,
            value=1,
            card_orders_touched=[0],
        ),
        Clue(
            player_index=other_player.index,
            is_color_clue=True,
            value=2,
            card_orders_touched=[1],
        ),
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


def test_clue_finder_rank_card(clue_finder):
    player = clue_finder.player
    player.add_card_to_hand(0, 1, 1)
    player.add_card_to_hand(1, 2, 2)
    player.add_card_to_hand(2, 1, 1)
    clue = Clue(
        player_index=player.index,
        is_color_clue=True,
        value=1,
        card_orders_touched=[0, 2]
    )
    assert clue_finder.clue_score(clue) == 2

    player.get_card(0).computed_info.touched = True
    assert clue_finder.clue_score(clue) == 1

    player.get_card(2).computed_info.touched = True
    assert clue_finder.clue_score(clue) == 0


def test_newly_touched_cards(clue_finder):
    player = clue_finder.player
    player.add_card_to_hand(0, 1, 1)
    player.add_card_to_hand(1, 2, 2)
    player.add_card_to_hand(2, 1, 1)
    clue = Clue(
        player_index=player.index,
        is_color_clue=True,
        value=1,
        card_orders_touched=[0, 2]
    )
    assert len(clue_finder.newly_touched_cards(clue)) == 2

    player.get_card(0).computed_info.touched = True
    assert len(clue_finder.newly_touched_cards(clue)) == 1

    player.get_card(2).computed_info.touched = True
    assert len(clue_finder.newly_touched_cards(clue)) == 0


def test_clue_follow_good_touch(clue_finder):
    player = clue_finder.player
    player.add_card_to_hand(0, 1, 1)
    player.add_card_to_hand(1, 2, 2)
    player.add_card_to_hand(2, 1, 1)
    clue = Clue(
        player_index=player.index,
        is_color_clue=True,
        value=1,
        card_orders_touched=[0, 2]
    )
    assert clue_finder.clue_follow_good_touch(clue)

    clue_finder.game.board.add_card(Card(1, 1, 1))
    assert not clue_finder.clue_follow_good_touch(clue)


def test_savable_cards_case_5(clue_finder):
    other_player = clue_finder.other_players()[0]
    other_player.add_card_to_hand(0, 1, 0)
    card_1 = other_player.get_card(0)
    other_player.add_card_to_hand(1, 5, 0)
    card_5 = other_player.get_card(1)
    assert clue_finder.savable_cards() == []

    card_1.computed_info.touched = True
    assert clue_finder.savable_cards() == [card_5]


def test_savable_cards_discard_interaction(clue_finder):
    other_player = clue_finder.other_players()[0]
    other_player.add_card_to_hand(0, 3, 0)
    assert clue_finder.savable_cards() == []

    clue_finder.game.board.discard_pile.append(Card(1, 0, 3))
    assert clue_finder.savable_cards() == [other_player.get_card(0)]


def test_get_focus_clue(clue_finder):
    other_player = clue_finder.other_players()[0]
    other_player.add_card_to_hand(0, 1, 1)
    other_player.add_card_to_hand(1, 1, 2)
    other_player.add_card_to_hand(2, 1, 3)
    other_player.add_card_to_hand(3, 1, 4)
    clue = Clue(
        player_index=other_player.index,
        is_color_clue=True,
        value=1,
        card_orders_touched=[0, 1, 2, 3]
    )
    assert clue_finder.get_focus_clue(clue) == other_player.get_chop()


def test_find_save_clues_case_5(clue_finder):
    other_player = clue_finder.other_players()[0]
    other_player.add_card_to_hand(0, 5, 0)
    save_clues = clue_finder.find_save_clues()
    assert save_clues == [Clue(
        player_index=other_player.index,
        is_color_clue=False,
        value=5,
        card_orders_touched=[0]
    )]


def test_find_save_clues_case_2(clue_finder):
    other_player = clue_finder.other_players()[0]
    other_player.add_card_to_hand(0, 2, 0)
    rank_save_clue = Clue(
        player_index=other_player.index,
        is_color_clue=False,
        value=2,
        card_orders_touched=[0]
    )
    color_save_clue = Clue(
        player_index=other_player.index,
        is_color_clue=True,
        value=0,
        card_orders_touched=[0]
    )
    assert clue_finder.find_save_clues() == [rank_save_clue]

    clue_finder.game.board.discard_pile.append(Card(1, 0, 2))
    assert len(clue_finder.find_save_clues()) == 2
    assert color_save_clue in clue_finder.find_save_clues()

    clue_finder.game.board.add_card(Card(1, 0, 1))
    clue_finder.game.board.add_card(Card(2, 0, 2))
    assert clue_finder.find_save_clues() == []


def test_find_save_clues_case_other(clue_finder):
    other_player = clue_finder.other_players()[0]
    other_player.add_card_to_hand(0, 3, 0)
    rank_save_clue = Clue(
        player_index=other_player.index,
        is_color_clue=False,
        value=3,
        card_orders_touched=[0]
    )
    color_save_clue = Clue(
        player_index=other_player.index,
        is_color_clue=True,
        value=0,
        card_orders_touched=[0]
    )
    assert clue_finder.find_save_clues() == []

    clue_finder.game.board.discard_pile.append(Card(1, 0, 3))
    assert len(clue_finder.find_save_clues()) == 2
    assert color_save_clue in clue_finder.find_save_clues()
    assert rank_save_clue in clue_finder.find_save_clues()

    clue_finder.game.board.add_card(Card(1, 0, 1))
    clue_finder.game.board.add_card(Card(2, 0, 2))
    clue_finder.game.board.add_card(Card(2, 0, 3))
    assert clue_finder.find_save_clues() == []


def test_filter_valid_play_clues(clue_finder):
    other_player = clue_finder.other_players()[0]
    other_player.add_card_to_hand(0, 3, 1)
    card_3 = other_player.get_card(0)
    play_clue = Clue(
        player_index=other_player.index,
        is_color_clue=True,
        value=1,
        card_orders_touched=[0]
    )
    clue_finder.game.board.add_card(Card(1, 1, 1))
    clue_finder.game.board.add_card(Card(2, 1, 2))

    assert clue_finder.game.board.is_card_valid(card_3)
    # The 3 is not critical, so it's a valid play clue
    assert clue_finder.filter_valid_play_clues([play_clue]) == [play_clue]

    clue_finder.game.board.discard_pile.append(Card(3, 1, 3))
    # The 3 is now critical, so it's seen as a save clue first and foremost
    assert clue_finder.filter_valid_play_clues([play_clue]) == []
