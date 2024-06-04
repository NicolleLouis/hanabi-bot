from services.player_finder import PlayerFinder


def test_clean_index(game):
    player_finder = PlayerFinder(game)
    assert player_finder.clean_index(0) == 0
    assert player_finder.clean_index(len(game.players) + 0) == 0
    assert player_finder.clean_index(len(game.players) + 1) == 1


def test_get_player(game):
    player_finder = PlayerFinder(game)
    assert player_finder.get_player(0) == game.players[0]


def test_next_seated_player_base_case(game):
    player_finder = PlayerFinder(game)
    game.own_index = 0
    assert player_finder.next_seated_player() == game.players[1]


def test_next_seated_player_case_specific_seat(game):
    player_finder = PlayerFinder(game)
    assert player_finder.next_seated_player(from_seat=0) == game.players[1]


def test_next_seated_player_case_skip(game):
    player_finder = PlayerFinder(game)
    game.own_index = 0
    assert player_finder.next_seated_player(skip=1) == game.player_finder.get_player(2)


def test_next_playing_player(game):
    player_finder = PlayerFinder(game)
    game.current_player_index = 0
    assert player_finder.next_playing_player() == game.players[1]
