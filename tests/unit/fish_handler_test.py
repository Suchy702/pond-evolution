import pytest

from src.object_handler.fish_handler import FishHandler
from src.object_kind import ObjectKind
# noinspection PyUnresolvedReferences
from tests.helper import get_object, INF, settings


@pytest.fixture
def fish_handler(settings):
    return FishHandler(settings)


def test_remove_dead_fish(fish_handler):
    dead_fish = get_object(ObjectKind.FISH)
    dead_fish.vitality = 0
    live_fish = get_object(ObjectKind.FISH)
    live_fish.vitality = 100
    fish_handler.add_all([dead_fish, live_fish])
    fish_handler.remove_dead_fish()
    assert fish_handler.size == 1


def test_breed_fish(fish_handler):
    father_fish = get_object(ObjectKind.FISH)
    fish_handler.add_all([father_fish])
    father_id = father_fish.id
    father_fish.vitality = INF
    fish_handler.breed_fish(father_fish)
    assert fish_handler.fishes[0].id != father_id
