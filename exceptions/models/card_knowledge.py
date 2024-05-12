from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from models.card_knowledge import CardKnowledge


class CardKnowledgeException(Exception):
    def __init__(self, card_knowledge: CardKnowledge, message="Unknown Error"):
        self.card_knowledge = card_knowledge
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.card_knowledge} -> {self.message}'
