import pytest

from src.object.fish import Fish
from src.position import Position


@pytest.fixture
def fish():
    return Fish(0, 0, Position(0, 0))


def test_spoil_vitality(fish):
    fish.spoil_vitality()
    assert fish.is_dead()


def test_birth(fish):
    born = fish.birth_fish()
    for f in born:
        assert id(f) != id(fish)
    assert fish.is_dead()
