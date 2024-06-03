import pytest

from models.client import Client


@pytest.fixture
def client() -> Client:
    return Client("None", "None")