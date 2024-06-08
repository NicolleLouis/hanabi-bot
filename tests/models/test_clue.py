from models.clue import Clue


def test_clue_equality():
    clue_1 = Clue(
        player_index=0,
        is_color_clue=True,
        value=0,
        card_orders_touched=[0, 1]
    )
    clue_2 = Clue(
        player_index=0,
        is_color_clue=True,
        value=0,
        card_orders_touched=[0, 1]
    )
    assert clue_1 == clue_2


def test_clue_inequality_case_player_index():
    clue_1 = Clue(
        player_index=0,
        is_color_clue=True,
        value=0,
        card_orders_touched=[0, 1]
    )
    clue_2 = Clue(
        player_index=1,
        is_color_clue=True,
        value=0,
        card_orders_touched=[0, 1]
    )
    assert not clue_1 == clue_2


def test_clue_inequality_case_type():
    clue_1 = Clue(
        player_index=0,
        is_color_clue=True,
        value=0,
        card_orders_touched=[0, 1]
    )
    clue_2 = Clue(
        player_index=0,
        is_color_clue=False,
        value=0,
        card_orders_touched=[0, 1]
    )
    assert not clue_1 == clue_2


def test_clue_inequality_case_value():
    clue_1 = Clue(
        player_index=0,
        is_color_clue=True,
        value=1,
        card_orders_touched=[0, 1]
    )
    clue_2 = Clue(
        player_index=0,
        is_color_clue=True,
        value=0,
        card_orders_touched=[0, 1]
    )
    assert not clue_1 == clue_2


def test_clue_inequality_case_order():
    clue_1 = Clue(
        player_index=0,
        is_color_clue=True,
        value=0,
        card_orders_touched=[1]
    )
    clue_2 = Clue(
        player_index=0,
        is_color_clue=True,
        value=0,
        card_orders_touched=[0, 1]
    )
    assert not clue_1 == clue_2
