# Replay: https://hanab.live/replay/1196641
from models.card.card import Card
from models.clue import Clue
from models.game import Game


# Red clue should not have been legal
def test_turn_14(client):
    game = Game(client)
    data = {
        "playerNames": ["LaFayetteBot1", "LaFayetteBot2", "LaFayetteX"],
        "ourPlayerIndex": 0,
        "tableID": "0",
    }
    game.start(data)
    la_fayette_x = game.player_finder.get_player(2)
    la_fayette_x.hand = [
        Card(0, 3, 5, game.deck),
        Card(1, 0, 2, game.deck),
        Card(2, 0, 4, game.deck),
        Card(3, 2, 4, game.deck),
        Card(4, 0, 3, game.deck),
    ]
    first_clue = Clue(
        player_index=2,
        is_color_clue=False,
        value=5,
        card_orders_touched=[0],
    )
    game.brain.receive_clue(clue=first_clue)

    second_clue = Clue(
        player_index=2,
        is_color_clue=False,
        value=2,
        card_orders_touched=[1],
    )
    game.brain.receive_clue(clue=second_clue)

    game.board.discard_pile.extend([
        Card(5, 0, 3, game.deck),
        Card(6, 4, 4, game.deck),
    ])

    save_clues = game.brain.find_save_clues()
    assert len(save_clues) == 0

    play_clues = game.brain.find_play_clues()
    assert len(play_clues) == 0
