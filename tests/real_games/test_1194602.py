# Replay: https://hanab.live/replay/1194602
from models.card.card import Card
from models.clue import Clue
from models.game import Game


def test_turn_23(client):
    game = Game(client)
    data = {
        "playerNames": ["LaFayetteBot2", "LaFayetteBot1", "LaFayetteX"],
        "ourPlayerIndex": 1,
        "tableID": "1",
    }
    game.start(data)
    game.ready()
    la_fayette_bot_1 = game.player_finder.get_player(1)
    game.board.discard_pile = [
        Card(0, 0, 1, game.deck),
        Card(1, 0, 4, game.deck),
        Card(2, 1, 4, game.deck),
        Card(3, 3, 4, game.deck),
    ]
    la_fayette_bot_1.hand = [
        Card(4, 4, 5, game.deck),
        Card(5, 0, 4, game.deck),
        Card(6, 1, 2, game.deck),
        Card(7, 3, 4, game.deck),
        Card(8, 0, 3, game.deck),
    ]
    first_clue = Clue(
        player_index=1,
        is_color_clue=False,
        value=5,
        card_orders_touched=[4],
    )
    game.brain.receive_clue(clue=first_clue)
    second_clue = Clue(
        player_index=1,
        is_color_clue=False,
        value=4,
        card_orders_touched=[5, 7],
    )
    game.brain.receive_clue(clue=second_clue)

    focused_card = la_fayette_bot_1.get_card(5)
    assert len(focused_card.computed_info.possible_cards) == 3
