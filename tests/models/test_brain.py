from models.card.physical_card import PhysicalCard
from models.clue import Clue


def test_good_touch_elimination(brain):
    brain.player.add_card_to_hand(0, 3, 3, deck=brain.game.deck)
    brain.player.add_card_to_hand(1, 1, 1, deck=brain.game.deck)
    brain.player.add_card_to_hand(2, 1, 2, deck=brain.game.deck)
    brain.player.add_card_to_hand(3, 3, 3, deck=brain.game.deck)
    clue = Clue(
        player_index=brain.player.index,
        is_color_clue=False,
        value=1,
        card_orders_touched=[1, 2]
    )
    brain.clue_receiver.receive_clue(clue=clue)
    assert brain.player.get_card(2).playable

    non_focus_1 = brain.player.get_card(1)
    assert not non_focus_1.playable
    assert non_focus_1.computed_info.possible_cards == {
        PhysicalCard(rank=1, suit=0),
        PhysicalCard(rank=1, suit=1),
        PhysicalCard(rank=1, suit=2),
        PhysicalCard(rank=1, suit=3),
        PhysicalCard(rank=1, suit=4)
    }

    brain.good_touch_elimination()
    brain.update_playability()
    assert non_focus_1.playable


def test_guess_trash_good_touch_elimination(brain):
    brain.player.add_card_to_hand(0, 1, 1, deck=brain.game.deck)
    card_1 = brain.player.get_card(0)
    clue = Clue(
        player_index=brain.player.index,
        is_color_clue=False,
        value=1,
        card_orders_touched=[0]
    )
    brain.clue_receiver.receive_clue(clue=clue)
    brain.good_touch_elimination()
    brain.update_playability()
    assert brain.player.get_card(0).playable

    brain.game.board.add_card(PhysicalCard(rank=1, suit=0))
    brain.game.board.add_card(PhysicalCard(rank=1, suit=1))
    brain.game.board.add_card(PhysicalCard(rank=1, suit=2))
    brain.game.board.add_card(PhysicalCard(rank=1, suit=3))
    brain.game.board.add_card(PhysicalCard(rank=1, suit=4))

    brain.good_touch_elimination()
    brain.update_playability()
    assert card_1.trash
    assert not card_1.playable
