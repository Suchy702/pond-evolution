import pytest

from src.object_handler.alga_handler import AlgaHandler
from src.object_kind import ObjectKind
from src.position import Position
from src.simulation_settings import SimulationSettings
from tests.helper import get_object


@pytest.fixture
def alga_handler():
    return AlgaHandler(SimulationSettings())


def test_kill_algae_on_surface(alga_handler):
    a1 = get_object(ObjectKind.ALGA, pos=Position(0, 1))
    a2 = get_object(ObjectKind.ALGA, pos=Position(2, 3))
    a3 = get_object(ObjectKind.ALGA, pos=Position(0, 2))
    a4 = get_object(ObjectKind.ALGA, pos=Position(0, 2))

    alga_handler.add_all([a1, a2, a3, a4])
    alga_handler.remove_algae_on_surface()

    assert alga_handler._object_database.size == 1
