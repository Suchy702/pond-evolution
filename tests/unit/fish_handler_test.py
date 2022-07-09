import pytest

from src.object_handler.fish_handler import FishHandler
from src.object_kind import ObjectKind
from src.simulation_settings import SimulationSettings
from tests.unit.helper import get_object

INF = 1_000_000_000


@pytest.fixture
def sample_fish_handler():
    return FishHandler(SimulationSettings(5, 5))


def test_remove_dead_fishes(sample_fish_handler):
    dead_fish = get_object(ObjectKind.FISH)
    dead_fish._vitality = 0
    live_fish = get_object(ObjectKind.FISH)
    live_fish._vitality = 100
    sample_fish_handler.add_all([dead_fish, live_fish])
    sample_fish_handler.remove_dead_fishes()
    assert sample_fish_handler.size == 1


def test_breed_fishes(sample_fish_handler):
    father_fish = get_object(ObjectKind.FISH)
    sample_fish_handler.add_all([father_fish])
    father_id = father_fish.id
    father_fish.vitality = INF
    sample_fish_handler.breed_fish()
    assert sample_fish_handler.fishes[0].id != father_id
