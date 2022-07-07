import pytest

from src.object_handler.alga_handler import AlgaeHandler
from src.object_kind import ObjectKind
from src.simulation_settings import SimulationSettings
from tests.unit.helper import get_object
from src.position import Position


@pytest.fixture
def sample_alg_h():
    return AlgaeHandler(SimulationSettings())


def test_del_algs_on_surface(sample_alg_h):
    a1 = get_object(ObjectKind.ALGA, pos=Position(0, 1))
    a2 = get_object(ObjectKind.ALGA, pos=Position(2, 3))
    a3 = get_object(ObjectKind.ALGA, pos=Position(0, 2))
    a33 = get_object(ObjectKind.ALGA, pos=Position(0, 2))
    sample_alg_h.add_all([a1, a2, a3, a33])
    sample_alg_h.kill_algae_on_surface()
    assert sample_alg_h._object_database.size == 1
