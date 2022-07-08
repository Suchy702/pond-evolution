import pytest

from src.object_handler.alga_handler import AlgaHandler
from src.object_kind import ObjectKind
from src.simulation_settings import SimulationSettings
from tests.unit.helper import get_object
from src.position import Position


@pytest.fixture
def sample_alga_handler():
    return AlgaHandler(SimulationSettings())


def test_kill_algae_on_surface(sample_alga_handler):
    a1 = get_object(ObjectKind.ALGA, pos=Position(0, 1))
    a2 = get_object(ObjectKind.ALGA, pos=Position(2, 3))
    a3 = get_object(ObjectKind.ALGA, pos=Position(0, 2))
    a4 = get_object(ObjectKind.ALGA, pos=Position(0, 2))

    sample_alga_handler.add_all([a1, a2, a3, a4])
    sample_alga_handler.remove_algae_on_surface()

    assert sample_alga_handler._object_database.size == 1
