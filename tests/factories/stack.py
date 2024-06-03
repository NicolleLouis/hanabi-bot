import random
from typing import Callable

import pytest
from models.stack import Stack


@pytest.fixture
def stack() -> Stack:
    suit = random.randint(1, 5)
    rank = random.randint(0, 5)
    stack = Stack(suit)
    stack.current_rank = rank
    return stack


@pytest.fixture
def stack_factory() -> Callable[[], Stack]:
    def _stack():
        suit = random.randint(1, 5)
        rank = random.randint(0, 5)
        stack = Stack(suit)
        stack.current_rank = rank
        return stack

    return _stack
