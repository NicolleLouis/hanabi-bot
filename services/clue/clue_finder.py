from __future__ import annotations

from typing import TYPE_CHECKING, List

from services.clue.clue_builder import ClueBuilder
from services.clue.clue_receiver import ClueReceiver

if TYPE_CHECKING:
    from models.clue import Clue
    from models.player import Player
    from models.card.card import Card
    from models.game import Game


class ClueFinderException(Exception):
    pass


class ClueFinder:
    def __init__(self, player: Player, game: Game):
        self.player = player
        self.game = game

    @property
    def brain(self):
        return self.game.brain

    def other_players(self):
        return [player for player in self.game.players if player != self.player]

    def find_play_clues(self) -> List[Clue]:
        playable_cards = self.playable_cards()
        touchable_cards = self.filter_touchable_cards(playable_cards)
        play_clues = []
        for card in touchable_cards:
            if self.is_card_color_focusable(card):
                play_clues.append(self.generate_clue(card, is_color_clue=True))
            if self.is_card_rank_focusable(card):
                play_clues.append(self.generate_clue(card, is_color_clue=False))
        valid_play_clues = self.filter_valid_play_clues(play_clues)
        valid_clues = self.filter_valid_clues(valid_play_clues)
        scored_play_clues = self.score_clues(valid_clues)
        return scored_play_clues

    def find_save_clues(self) -> List[Clue]:
        savable_cards = self.savable_cards()

        save_clues = []
        for card in savable_cards:
            save_clues.append(self.generate_clue(card, is_color_clue=True))
            save_clues.append(self.generate_clue(card, is_color_clue=False))
        valid_save_clues = self.filter_valid_save_clues(save_clues)
        valid_clues = self.filter_valid_clues(valid_save_clues)
        scored_save_clues = self.score_clues(valid_clues)
        return scored_save_clues

    def score_clues(self, clues: List[Clue]) -> List[Clue]:
        for clue in clues:
            clue.score = self.clue_score(clue)
        return clues

    def filter_valid_save_clues(self, clues: List[Clue]) -> List[Clue]:
        valid_save_clues = []
        for clue in clues:
            card_saved = self.get_focus_clue(clue)
            if card_saved.rank == 5 and clue.is_color_clue:
                continue
            if card_saved.rank == 2 and clue.is_color_clue and not self.game.board.is_critical(card_saved):
                continue
            valid_save_clues.append(clue)
        return valid_save_clues

    def filter_valid_clues(self, clues: List[Clue]) -> List[Clue]:
        validation_function = [
            self.clue_follow_minimum_value,
            self.clue_follow_good_touch,
            self.clue_should_not_duplicate_cards,
        ]
        filtered_clues = clues
        for function in validation_function:
            filtered_clues = [clue for clue in filtered_clues if function(clue)]
        return filtered_clues

    def filter_valid_play_clues(self, clues: List[Clue]) -> List[Clue]:
        valid_play_clues = []
        clue_receiver = ClueReceiver(self.game)
        for clue in clues:
            if not clue_receiver.is_legal_save_clue(clue):
                valid_play_clues.append(clue)
        return valid_play_clues

    def filter_touchable_cards(self, cards: List[Card]):
        touchable_cards = []
        for card in cards:
            if self.is_card_color_focusable(card) or self.is_card_rank_focusable(card):
                touchable_cards.append(card)
        return touchable_cards

    # Fetch only chop cards
    def savable_cards(self) -> List[Card]:
        savable_cards = []
        for player in self.other_players():
            card = player.get_chop()
            if card is None:
                continue
            if self.game.board.is_critical(card.physical_card):
                savable_cards.append(card)
                continue
            if card.rank == 2 and not self.game.board.is_already_played(card.physical_card):
                savable_cards.append(card)
        return savable_cards

    def playable_cards(self) -> List[Card]:
        playable_cards = []
        for player in self.other_players():
            for card in player.hand:
                if self.game.board.is_card_valid(card):
                    playable_cards.append(card)
        return playable_cards

    def generate_clue(self, card: Card, is_color_clue: bool) -> Clue:
        other_players = self.other_players()
        players_with_card = [player for player in other_players if player.has_card(card)]
        if len(players_with_card) == 0:
            raise ClueFinderException('Card not found in other players hands')
        player = players_with_card[0]
        return ClueBuilder.generate_clue(
            player=player,
            is_color_clue=is_color_clue,
            card=card
        )

    def get_focus_clue(self, clue: Clue) -> Card:
        return ClueReceiver(self.game).find_focus(clue)

    def is_card_color_focusable(self, card: Card) -> bool:
        color_clue = self.generate_clue(
            card=card,
            is_color_clue=True
        )
        return self.get_focus_clue(color_clue) == card

    def is_card_rank_focusable(self, card: Card) -> bool:
        rank_clue = self.generate_clue(
            card=card,
            is_color_clue=False
        )
        return self.get_focus_clue(rank_clue) == card

    def clue_follow_good_touch(self, clue: Clue) -> bool:
        newly_touched_cards = self.newly_touched_cards(clue)
        known_cards = self.brain.get_cards_gotten()
        for card in newly_touched_cards:
            if card.physical_card in known_cards:
                return False
        return True

    def clue_follow_minimum_value(self, clue: Clue) -> bool:
        return len(self.newly_touched_cards(clue)) > 0

    def clue_should_not_duplicate_cards(self, clue: Clue) -> bool:
        touched_cards = self.touched_cards(clue)
        touched_physical_cards = [card.physical_card for card in touched_cards]
        return len(touched_physical_cards) == len(set(touched_physical_cards))

    def touched_cards(self, clue: Clue) -> List[Card]:
        clued_player = self.game.player_finder.get_player(clue.player_index)
        return [card for card in clued_player.hand if card.order in clue.card_orders_touched]

    def newly_touched_cards(self, clue: Clue) -> List[Card]:
        touched_cards = self.touched_cards(clue)
        return [card for card in touched_cards if not card.touched]

    # 1 point per card newly touched
    def clue_score(self, clue: Clue) -> int:
        newly_touched_card = self.newly_touched_cards(clue)
        return len(newly_touched_card)
