from __future__ import annotations

import random
from collections import Counter
from typing import TYPE_CHECKING, Optional, List, Union

from constants.action_source import ActionSource
from models.action import Action
from models.card.card import Card
from models.thought import Thought
from services.clue.clue_finder import ClueFinder
from services.clue.clue_receiver import ClueReceiver
from services.discard import DiscardService
from services.play import PlayService
from models.clue import Clue

if TYPE_CHECKING:
    from models.card.physical_card import PhysicalCard
    from models.game import Game
    from models.player import Player


class Brain:
    def __init__(self, game: Game):
        self.game = game
        self.player = None
        self.discard_service: Optional[DiscardService] = None
        self.play_service: Optional[PlayService] = None
        self.clue_receiver: ClueReceiver = ClueReceiver(game)
        self.clue_finder: Optional[ClueFinder] = None
        self.memory: List[Thought] = []

    # Main Action loop
    def find_action(self):
        self.update_state()
        actions = self.find_potential_actions()
        thought = self.get_thought(self.game.turn_number)
        thought.actions = actions
        return self.choose_action(actions)

    def get_thought(self, turn: Optional[Union[int, str]] = None) -> Thought:
        if turn is None:
            turn = self.game.turn_number
        if isinstance(turn, str):
            turn = int(turn)
        for thought in self.memory:
            if thought.turn == turn:
                return thought
        self.create_thought(turn)
        return self.get_thought(turn)

    def other_players(self):
        return [player for player in self.game.players if player != self.player]

    def create_thought(self, turn: int) -> None:
        thought = Thought(turn=turn)
        self.memory.append(thought)

    def display_thought(self, turn):
        thought = self.get_thought(turn)
        thought.pretty_print()

    def find_potential_actions(self) -> List[Action]:
        potential_actions = []
        potential_actions.extend(self.find_play_actions())
        potential_actions.extend(self.find_discard_actions())
        potential_actions.extend(self.find_play_clues())
        potential_actions.extend(self.find_save_clues())
        potential_actions.extend(self.find_stall_clues())
        return potential_actions

    def find_play_actions(self) -> List[Action]:
        play_actions = []
        for card in self.player.hand:
            card.update_playability(self.game.board)
            if card.computed_info.playable:
                play_actions.append(self.play_service.to_card(card, 2))
        return play_actions

    def find_discard_actions(self) -> List[Action]:
        discard_actions = [self.discard_service.to_chop(0)]
        for card in self.player.trash_cards:
            discard_actions.append(self.discard_service.to_card(card, 1))
        return discard_actions

    def find_stall_clues(self) -> List[Action]:
        stall_clues = self.clue_finder.find_stall_clues()
        stall_clue_actions = []
        for clue in stall_clues:
            stall_clue_actions.append(clue.to_action(ActionSource.STALL_CLUE))
        return stall_clue_actions

    def find_play_clues(self) -> List[Action]:
        play_clues = self.clue_finder.find_play_clues()
        play_clue_actions = []
        for clue in play_clues:
            play_clue_actions.append(clue.to_action(ActionSource.PLAY_CLUE))
        return play_clue_actions

    def find_save_clues(self) -> List[Action]:
        save_clues = self.clue_finder.find_save_clues()
        save_clue_actions = []
        for clue in save_clues:
            save_clue_actions.append(clue.to_action(ActionSource.SAVE_CLUE))
        return save_clue_actions

    def choose_action(self, actions: List[Action]) -> Action:
        actions = [action for action in actions if action is not None]
        impossible_actions = []
        if self.game.clue_tokens == 0:
            impossible_actions = [
                ActionSource.PLAY_CLUE,
                ActionSource.SAVE_CLUE,
                ActionSource.STALL_CLUE,
            ]
        elif self.game.clue_tokens == 8:
            impossible_actions = [
                ActionSource.DISCARD,
            ]
        actions = [action for action in actions if action.source not in impossible_actions]
        max_score = max([action.score for action in actions])
        best_actions = [action for action in actions if action.score == max_score]
        return random.choice(best_actions)

    def discard(self):
        trash_cards = self.player.trash_cards
        if len(trash_cards) > 0:
            return self.discard_service.to_card(trash_cards[-1])
        return self.discard_service.to_chop()

    def set_player(self, player: Player):
        self.player = player
        self.discard_service = DiscardService(player)
        self.play_service = PlayService(player)
        self.clue_finder = ClueFinder(player, self.game)

    @property
    def player_finder(self):
        return self.game.player_finder

    def has_playable_cards(self):
        return len(self.player.playable_cards) > 0

    def display_card_options(self):
        print("Card Options:")
        for card in self.player.hand:
            print(card)
            card.computed_info.pretty_print()

    # Beware touched cards by ourselves (Might be duplicated)
    def get_cards_gotten(self) -> List[PhysicalCard]:
        played_cards = self.game.board.get_played_cards()
        touched_cards = []
        for player in self.other_players():
            touched_cards.extend([card.physical_card for card in player.touched_cards])
        known_cards = self.player.known_cards
        known_physical_cards = [card.physical_card for card in known_cards]
        return played_cards + touched_cards + known_physical_cards

    def good_touch_elimination(self):
        cards_gotten = self.get_cards_gotten()
        for card in self.player.touched_cards:
            for card_gotten in cards_gotten:
                if card.physical_card != card_gotten:
                    card.computed_info.remove_possibility(card_gotten)

    def visible_cards(self):
        visible_cards = self.game.board.discard_pile + self.game.board.get_played_cards()
        for player in self.game.players:
            if player != self.player:
                visible_cards.extend(player.hand)

        visible_cards = [
            card.physical_card if isinstance(card, Card) else card for card in visible_cards
        ]
        return visible_cards

    def remaining_cards(self):
        deck_counter = Counter(self.game.deck.cards)
        visible_counter = Counter(self.visible_cards())

        remaining_counter = deck_counter - visible_counter

        return list(remaining_counter.elements())

    def visible_cards_elimination(self):
        for card in self.player.hand:
            card_possibilities = set(card.computed_info.possible_cards)
            for possible_card in card_possibilities:
                if possible_card not in self.remaining_cards():
                    card.computed_info.remove_possibility(possible_card)

    def update_playability(self):
        for card in self.player.hand:
            card.update_playability(self.game.board)

    def receive_clue(self, data: Optional[dict] = None, clue: Optional[Clue] = None):
        if clue is None:
            clue = Clue(data)
        self.clue_receiver.receive_clue(
            clue=clue
        )
        self.update_state()
        thought = self.get_thought()
        target_player = self.player_finder.get_player(clue.player_index)
        thought.set_touched_player(target_player)

    def update_state(self):
        self.good_touch_elimination()
        self.visible_cards_elimination()
        self.update_playability()
        self.get_thought(self.game.turn_number).set_hand(self.player.hand)
