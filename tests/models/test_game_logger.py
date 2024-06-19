import json
import os


def test_save(game):
    game.logger.log({"event": "test"})
    game.table_id = "test"
    game.player_finder.find_self().name = "test"
    game.logger.save()

    filename = "test-test.json"
    full_path = "game_files/test-test.json"
    assert game.logger.file_name == filename
    assert os.path.exists(full_path)

    with open(full_path, "r") as f:
        logs = json.load(f)
        assert logs == [{"event": "test"}]
