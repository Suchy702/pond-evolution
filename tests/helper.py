import pytest

from src.object.alga import Alga
from src.object.alga_maker import AlgaMaker
from src.object.fish import Fish
from src.object.object_kind import ObjectKind
from src.object.worm import Worm
from src.position import Position
from src.simulation_settings import SimulationSettings

INF = 1_000_000_000


def get_object(kind=ObjectKind.FISH, pos=Position(0, 0), speed=10, size=10, energy_val=15, pond_dim=(90, 160)):
    objects = {
        ObjectKind.FISH: Fish(speed, size, 10, pos),
        ObjectKind.WORM: Worm(energy_val, pos, pond_dim),
        ObjectKind.ALGA: Alga(energy_val, pos, pond_dim[0]),
        ObjectKind.ALGA_MAKER: AlgaMaker(pos, pond_dim[0]),
    }
    return objects[kind]


@pytest.fixture
def settings():
    s = SimulationSettings()
    s.pond_width = 5
    s.pond_height = 5
    s.no_worms_from_heaven = False
    return s


@pytest.fixture
def pond_object():
    return get_object()
