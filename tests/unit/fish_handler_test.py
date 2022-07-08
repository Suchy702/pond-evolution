import pytest

from tests.unit.helper import get_object

from src.object_handler.fish_handler import FishHandler
from src.simulation_settings import SimulationSettings
from src.object_kind import ObjectKind


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
