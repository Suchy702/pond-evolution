import pytest

from src.engine import Engine
from src.object_kind import ObjectKind
from src.simulation_settings import SimulationSettings
from tests.unit.helper import get_object
from src.position import Position


@pytest.fixture
def sample_engine():
    return Engine(SimulationSettings())


def test_find_pos_where_eat_when_fish_and_worm(sample_engine):
    w_1_1 = get_object(ObjectKind.WORM, pos=Position(1, 1))
    f_1_1 = get_object(ObjectKind.FISH, pos=Position(1, 1))
    sample_engine._fish_handler.add_all([f_1_1])
    sample_engine._worm_handler.add_all([w_1_1])
    assert sample_engine._find_pos_where_eat()[0] == Position(1, 1)


def test_find_pos_where_eat_when_fish_and_alg(sample_engine):
    a_1_1 = get_object(ObjectKind.ALGA, pos=Position(1, 1))
    f_1_1 = get_object(ObjectKind.FISH, pos=Position(1, 1))
    sample_engine._fish_handler.add_all([f_1_1])
    sample_engine._worm_handler.add_all([a_1_1])
    assert sample_engine._find_pos_where_eat()[0] == Position(1, 1)


def test_eat_at_one_spot(sample_engine):
    w = get_object(ObjectKind.WORM, pos=Position(1, 1), energy_val=10)
    a = get_object(ObjectKind.ALGA, pos=Position(1, 1), energy_val=20)
    f1 = get_object(ObjectKind.FISH, pos=Position(1, 1))
    f2 = get_object(ObjectKind.FISH, pos=Position(1, 1))
    f1.vitality = 0
    f2.vitality = 0
    sample_engine._worm_handler.add_all([w])
    sample_engine._plant_handler.alga_handler.add_all([a])
    sample_engine._fish_handler.add_all([f1, f2])
    sample_engine._eat_at_one_spot(Position(1, 1))
    assert f1.vitality == 15 and f2.vitality == 15
