from models.clue import Clue
from services.clue.clue_builder import ClueBuilder


def test_generate_color_clue(empty_handed_player):
    expected_clue = Clue(
        player_index=empty_handed_player.index,
        is_color_clue=True,
        value=0,
        card_orders_touched=[0, 1]
    )
    empty_handed_player.add_card_to_hand(0, 1, 0)
    empty_handed_player.add_card_to_hand(1, 2, 0)
    empty_handed_player.add_card_to_hand(2, 2, 1)
    clue = ClueBuilder.generate_clue(empty_handed_player, is_color_clue=True, card=empty_handed_player.get_card(0))
    assert clue == expected_clue


def test_generate_rank_clue(empty_handed_player):
    expected_clue = Clue(
        player_index=empty_handed_player.index,
        is_color_clue=False,
        value=2,
        card_orders_touched=[1, 2]
    )
    empty_handed_player.add_card_to_hand(0, 1, 0)
    empty_handed_player.add_card_to_hand(1, 2, 0)
    empty_handed_player.add_card_to_hand(2, 2, 1)
    clue = ClueBuilder.generate_clue(
        empty_handed_player,
        is_color_clue=False,
        card=empty_handed_player.get_card(2)
    )
    assert clue == expected_clue
