from __future__ import annotations

from typing import List
from models.game import Game
from models.action import Action


class GameBuilderException(Exception):
    pass


class GameBuilder:
    def __init__(self, raw_data: List[dict]):
        self.raw_data = raw_data.copy()
        self.game = Game(builder=self)
        self.game.forced_action = True
        self.next_action = None

    def build_until_turn(self, turn_number: int) -> None:
        while self.game.turn_number < turn_number:
            self.build_next()

    def build_until_end(self) -> None:
        while self.raw_data:
            self.build_next()

    def set_next_action(self) -> None:
        if self.next_action is not None:
            return
        next_raw_action = next(filter(
            lambda item: 'action' in item,
            self.raw_data
        ), None)
        if next_raw_action is None:
            raise GameBuilderException("No more actions to build")
        next_raw_action = next_raw_action['action']
        self.next_action = Action(
            action_type=next_raw_action['action_type'],
            target=next_raw_action['target'],
            value=next_raw_action['value'],
        )

    def get_next_action(self) -> Action:
        if self.next_action is None:
            self.set_next_action()
        next_action = self.next_action
        self.next_action = None
        return next_action

    def build_next_draw(self, next_event: dict) -> None:
        data = next_event['draw']
        self.game.draw(data)

    def build_ready(self, next_event: dict) -> None:
        if next_event['game'] != 'ready':
            raise GameBuilderException("Strange payload for ready event")
        self.game.ready()

    def build_next_action(self, _next_event: dict) -> None:
        return

    def build_next_turn(self, next_event: dict) -> None:
        data = next_event['turn']
        self.game.turn(data)

    def build_next_play(self, next_event: dict) -> None:
        data = next_event['play']
        self.game.play(data)

    def build_next_clue(self, next_event: dict) -> None:
        data = next_event['clue']
        self.game.clue(data)

    def build_next_discard(self, next_event: dict) -> None:
        data = next_event['discard']
        self.game.discard(data)

    def build_next_strike(self, next_event: dict) -> None:
        data = next_event['strike']
        self.game.strike(data)

    def build_start(self, next_event: dict) -> None:
        data = next_event['start']
        self.game.start(data)

    def build_next(self) -> None:
        next_event = self.get_next_event()
        if 'start' in next_event:
            self.build_start(next_event)
        elif 'draw' in next_event:
            self.build_next_draw(next_event)
        elif 'game' in next_event:
            self.build_ready(next_event)
        elif 'action' in next_event:
            self.build_next_action(next_event)
        elif 'turn' in next_event:
            self.build_next_turn(next_event)
        elif 'play' in next_event:
            self.build_next_play(next_event)
        elif 'clue' in next_event:
            self.build_next_clue(next_event)
        elif 'discard' in next_event:
            self.build_next_discard(next_event)
        elif 'strike' in next_event:
            self.build_next_strike(next_event)
        else:
            raise NotImplementedError

    def export_game(self) -> Game:
        self.game.forced_action = False
        return self.game

    def get_next_event(self):
        return self.raw_data.pop(0)
