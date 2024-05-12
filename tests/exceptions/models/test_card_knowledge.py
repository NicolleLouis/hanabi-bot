from exceptions.models.card_knowledge import CardKnowledgeException
from models.card_knowledge import CardKnowledge


def test_str():
    card_knowledge = CardKnowledge()
    exception = CardKnowledgeException(card_knowledge, message="Test")
    assert exception.card_knowledge == card_knowledge
    assert exception.message == "Test"
    assert str(exception) == 'Unknown: 5 colors possible and 5 potential values -> Test'
