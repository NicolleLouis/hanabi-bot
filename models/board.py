from __future__ import annotations

from typing import Optional, List, TYPE_CHECKING, Union

from services.card import CardService

if TYPE_CHECKING:
    from models.game import Game

from models.card.card import Card
from services.deck import DeckService
from models.card.physical_card import PhysicalCard
from models.stack import Stack


class BoardException(Exception):
    pass


class Board:
    def __init__(self, game: Game, suits: Optional[List[int]] = None):
        self.game = game
        self.discard_pile: List[Card] = []
        self.deck_service = DeckService(game.deck)

        self.stacks: List[Stack] = []
        for suit in suits:
            self.stacks.append(Stack(suit))

    def __str__(self):
        return f"Board: {' '.join(map(str, self.stacks))}"

    @property
    def deck(self):
        return self.game.deck

    def add_card(self, card: PhysicalCard):
        for stack in self.stacks:
            if stack.add_card(card):
                return True
        return False

    def is_card_valid(self, card: PhysicalCard):
        stack = self.get_stack(card.suit)
        return stack.is_card_valid(card)

    def get_stack(self, suit: int) -> Stack:
        for stack in self.stacks:
            if stack.suit == suit:
                return stack
        raise BoardException(f"Stack with suit {suit} not found")

    def is_already_played(self, card: PhysicalCard):
        stack = self.get_stack(card.suit)
        return card in stack.played_cards

    def get_played_cards(self):
        played_cards = []
        for stack in self.stacks:
            played_cards.extend(stack.played_cards)
        return played_cards

    def get_playable_rank(self, suit: int) -> Optional[int]:
        stack = self.get_stack(suit)
        return stack.get_playable_rank()

    def get_playable_suits(self, rank: int) -> Optional[List[int]]:
        playable_suits = []
        for stack in self.stacks:
            if stack.is_card_valid(PhysicalCard(suit=stack.suit, rank=rank)):
                playable_suits.append(stack.suit)
        return playable_suits

    def is_critical(self, card: Union[PhysicalCard, Card]):
        if isinstance(card, Card):
            card = card.physical_card
        cleaned_discard_pile = CardService.convert_to_physical_cards(self.discard_pile)
        return self.deck_service.is_card_critical(card, cleaned_discard_pile)
