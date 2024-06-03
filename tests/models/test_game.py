from models.game import Game


def test_start_game(client):
    game = Game(client)
    data = {
        "playerNames": ["Alice", "Bob", "Charlie"],
        "ourPlayerIndex": 1,
        "tableID": "table1"
    }
    game.start(data)

    assert game.table_id == "table1"
    assert game.turn == -1
    assert game.own_index == 1
    assert len(game.players) == 3


def test_get_players(game):
    assert game.get_players(0).name == game.players[0].name
