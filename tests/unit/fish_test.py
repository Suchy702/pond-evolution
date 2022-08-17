import pytest

from src.object.fish import Fish
from src.position import Position


@pytest.fixture
def fish():
    fish = Fish(0, 0, 0, Position(0, 0))
    fish.vitality = 0
    return fish


def test_spoil_vitality(fish):
    fish.spoil_vitality(100, 100)
    assert not fish.is_alive()


def test_birth(fish):
    born = fish.birth_fish()
    for f in born:
        assert id(f) != id(fish)
    assert not fish.is_alive()
