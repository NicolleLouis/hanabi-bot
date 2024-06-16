# Replay: https://hanab.live/replay/1194473
from models.card.card import Card
from models.clue import Clue
from models.game import Game


def test_turn_4(client):
    game = Game(client)
    data = {
        "playerNames": ["LaFayetteBot1", "LaFayetteBot2", "LaFayetteX"],
        "ourPlayerIndex": 0,
        "tableID": "1",
    }
    game.start(data)
    la_fayette_x = game.player_finder.get_player(2)
    la_fayette_x.hand = [
        Card(0, 4, 5, game.deck),
        Card(1, 2, 5, game.deck),
        Card(2, 4, 1, game.deck),
        Card(3, 3, 1, game.deck),
        Card(4, 3, 3, game.deck),
    ]
    first_clue = Clue(
        player_index=2,
        is_color_clue=False,
        value=1,
        card_orders_touched=[2, 3],
    )
    game.brain.receive_clue(clue=first_clue)

    second_clue = Clue(
        player_index=2,
        is_color_clue=False,
        value=5,
        card_orders_touched=[0, 1],
    )
    game.brain.receive_clue(clue=second_clue)

    play_data = {
        "playerIndex": 2,
        "order": 2,
        "suitIndex": 4,
        "rank": 1,
    }
    game.play(play_data)
    draw_data = {
        "playerIndex": 2,
        "order": 5,
        "suitIndex": 3,
        "rank": 2,
    }
    game.draw(draw_data)

    faulty_clue = Clue(
        player_index=2,
        is_color_clue=True,
        value=3,
        card_orders_touched=[4, 5, 3],
    )
    assert game.brain.clue_receiver.find_focus(faulty_clue) == la_fayette_x.get_card(4)

    play_clues = game.brain.find_play_clues()
    assert len(play_clues) == 0

    save_clues = game.brain.find_save_clues()
    assert len(save_clues) == 0
