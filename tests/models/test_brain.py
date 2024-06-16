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


def test_no_good_touch_elimination_on_untouched_card(brain):
    brain.player.add_card_to_hand(0, -1, -1, deck=brain.game.deck)
    unplayable_card = brain.player.get_card(0)

    for suit in range(1, 5):
        brain.player.add_card_to_hand(suit, 1, suit, deck=brain.game.deck)
        brain.clue_receiver.receive_clue(clue=Clue(
            player_index=brain.player.index,
            is_color_clue=True,
            value=suit,
            card_orders_touched=[suit]
        ))

    brain.good_touch_elimination()
    brain.update_playability()
    assert not unplayable_card.playable

    brain.game.board.add_card(PhysicalCard(rank=1, suit=0))
    brain.game.board.add_card(PhysicalCard(rank=2, suit=0))
    brain.game.board.add_card(PhysicalCard(rank=3, suit=0))
    brain.game.board.add_card(PhysicalCard(rank=4, suit=0))

    brain.good_touch_elimination()
    brain.update_playability()
    assert not unplayable_card.playable
    assert len(unplayable_card.computed_info.possible_cards) == 5


# ToDo Random fails here
def test_get_known_cards(brain):
    assert brain.get_known_cards() == []

    brain.game.board.add_card(PhysicalCard(rank=1, suit=0))
    assert brain.get_known_cards() == [PhysicalCard(rank=1, suit=0)]

    brain.player.add_card_to_hand(0, 1, 1, deck=brain.game.deck)
    brain.player.get_card(0).computed_info.touched = True
    assert brain.get_known_cards() == [
        PhysicalCard(rank=1, suit=0),
        PhysicalCard(rank=1, suit=1)
    ]

    next_player = brain.player_finder.next_seated_player()
    next_player.add_card_to_hand(1, 1, 2, deck=brain.game.deck)
    next_player.get_card(1).computed_info.touched = True
    assert brain.get_known_cards() == [
        PhysicalCard(rank=1, suit=0),
        PhysicalCard(rank=1, suit=1),
        PhysicalCard(rank=1, suit=2),
    ]


def test_visible_cards(brain):
    assert brain.visible_cards() == []

    brain.player.add_card_to_hand(0, 1, 1, deck=brain.game.deck)
    assert brain.visible_cards() == []

    brain.game.board.add_card(PhysicalCard(rank=1, suit=0))
    assert brain.visible_cards() == [PhysicalCard(rank=1, suit=0)]

    next_player = brain.player_finder.next_seated_player()
    next_player.add_card_to_hand(1, 1, 2, deck=brain.game.deck)
    assert len(brain.visible_cards()) == 2
    assert PhysicalCard(rank=1, suit=2) in brain.visible_cards()

    brain.game.board.discard_pile.append(PhysicalCard(rank=1, suit=3))
    assert len(brain.visible_cards()) == 3
    assert PhysicalCard(rank=1, suit=3) in brain.visible_cards()


def test_remaining_cards(brain):
    assert len(brain.remaining_cards()) == 50

    brain.player.add_card_to_hand(0, 1, 1, deck=brain.game.deck)
    assert len(brain.remaining_cards()) == 50

    brain.game.board.add_card(PhysicalCard(rank=1, suit=1))
    assert len(brain.remaining_cards()) == 49

    next_player = brain.player_finder.next_seated_player()
    next_player.add_card_to_hand(1, 1, 1, deck=brain.game.deck)
    assert len(brain.remaining_cards()) == 48

    brain.game.board.discard_pile.append(PhysicalCard(rank=1, suit=1))
    assert len(brain.remaining_cards()) == 47
    assert PhysicalCard(rank=1, suit=1) not in brain.remaining_cards()


def test_visible_card_elimination(brain):
    brain.player.add_card_to_hand(0, -1, -1, deck=brain.game.deck)
    card = brain.player.get_card(0)
    card.computed_info.possible_cards = {
        PhysicalCard(rank=1, suit=0),
        PhysicalCard(rank=2, suit=0),
        PhysicalCard(rank=3, suit=0),
        PhysicalCard(rank=4, suit=0),
        PhysicalCard(rank=5, suit=0)
    }
    card.computed_info.touched = True

    brain.game.board.add_card(PhysicalCard(rank=1, suit=0))
    brain.game.board.add_card(PhysicalCard(rank=2, suit=0))
    brain.game.board.add_card(PhysicalCard(rank=3, suit=0))

    brain.good_touch_elimination()
    assert card.computed_info.possible_cards == {
        PhysicalCard(rank=4, suit=0),
        PhysicalCard(rank=5, suit=0)
    }

    next_player = brain.player_finder.next_seated_player()
    next_player.add_card_to_hand(1, 5, 0, deck=brain.game.deck)
    brain.visible_cards_elimination()

    assert card.computed_info.possible_cards == {
        PhysicalCard(rank=4, suit=0)
    }
