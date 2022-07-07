import pytest

from src.object_handler.worm_handler import WormHandler
from src.object_kind import ObjectKind
from src.simulation_settings import SimulationSettings
from tests.unit.helper import get_object
from src.position import Position


@pytest.fixture
def settings():
    s = SimulationSettings()
    s.pond_width = 10
    s.pond_height = 5
    return s


@pytest.fixture
def sample_worm_handler(settings):
    return WormHandler(settings)


def test_del_worms_from_ground(sample_worm_handler):
    w1 = get_object(ObjectKind.WORM, pos=Position(4, 5))
    w2 = get_object(ObjectKind.WORM, pos=Position(0, 2))
    w3 = get_object(ObjectKind.WORM, pos=Position(4, 2))
    w4 = get_object(ObjectKind.WORM, pos=Position(4, 2))

    sample_worm_handler.add_all([w1, w2, w3, w4])
    sample_worm_handler.del_worms_from_ground()

    assert sample_worm_handler._object_database.size == 1
