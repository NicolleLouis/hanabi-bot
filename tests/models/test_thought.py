from unittest.mock import patch

from constants.actions import ACTION
from models.action import Action
from models.card.card import Card
from models.card.computed_info import ComputedInfo
from models.thought import Thought


@patch.object(Action, '__str__', return_value="Detailed Action")
@patch('builtins.print')
def test_pretty_print_action(mock_print, _mock_str):
    thought = Thought(0)
    action = Action(ACTION.PLAY, 1)
    thought.actions = [action]
    thought.pretty_print_actions()
    mock_print.assert_any_call("Action: ")
    mock_print.assert_any_call("Detailed Action")


@patch.object(Thought, 'pretty_print_hand')
@patch.object(Thought, 'pretty_print_actions')
@patch('builtins.print')
def test_pretty_print(_print, mock_pretty_print_actions, mock_pretty_print_hand):
    thought = Thought(0)
    thought.pretty_print()
    mock_pretty_print_actions.assert_called_once()
    mock_pretty_print_hand.assert_called()


@patch.object(ComputedInfo, 'display_possibilities')
@patch('builtins.print')
def test_pretty_print_hand(mock_print, mock_display_possibilities):
    thought = Thought(0)
    thought.pretty_print_hand()
    mock_print.assert_not_called()

    card = Card(0, 1, 1)
    thought.set_hand([card])
    thought.pretty_print_hand()
    mock_print.assert_not_called()

    card.is_known = True
    thought.pretty_print_hand()
    # Hand was copied so changing the card afterward has no impact
    mock_print.assert_not_called()

    thought.hand = [card]
    thought.pretty_print_hand()
    mock_print.assert_called_with("Slot 1: Known Card: 1 of 1")
    mock_display_possibilities.assert_not_called()

    card.is_known = False
    card.computed_info.touched = True
    thought.pretty_print_hand()
    mock_print.assert_called_with("Slot 1: Touched Card with 0 possibilities")
    mock_display_possibilities.assert_called()
