import pytest

from services.action import ActionService, ActionServiceException


def test_translate_action():
    expected_result = {
        0: 'Play',
        1: 'Discard',
        2: 'Color Clue',
        3: 'Rank Clue',
    }
    for raw_input, expected_result in expected_result.items():
        assert ActionService.translate_action(str(raw_input)) == expected_result


def test_translate_action_case_unknown():
    with pytest.raises(ActionServiceException):
        ActionService.translate_action('5')
