import pytest

from src.logic.interactor import Interactor
from src.object.object_kind import ObjectKind
from src.position import Position
# noinspection PyUnresolvedReferences
from tests.helper import get_object, settings


@pytest.fixture
def interactor(settings):
    return Interactor(settings)


def test_find_pos_where_eat_when_fish_and_worm(interactor):
    w_1_1 = get_object(ObjectKind.WORM, pos=Position(1, 1))
    f_1_1 = get_object(ObjectKind.FISH, pos=Position(1, 1))
    interactor._fish_handler.add_all([f_1_1])
    interactor._worm_handler.add_all([w_1_1])
    assert interactor._find_pos_where_eat()[0] == Position(1, 1)


def test_find_pos_where_eat_when_fish_and_alg(interactor):
    a_1_1 = get_object(ObjectKind.ALGA, pos=Position(1, 1))
    f_1_1 = get_object(ObjectKind.FISH, pos=Position(1, 1))
    interactor._fish_handler.add_all([f_1_1])
    interactor._worm_handler.add_all([a_1_1])
    assert interactor._find_pos_where_eat()[0] == Position(1, 1)


def test_eat_at_one_spot(interactor):
    w = get_object(ObjectKind.WORM, pos=Position(1, 1), energy_val=10)
    a = get_object(ObjectKind.ALGA, pos=Position(1, 1), energy_val=20)
    f1 = get_object(ObjectKind.FISH, pos=Position(1, 1))
    f2 = get_object(ObjectKind.FISH, pos=Position(1, 1))
    f1.vitality = 0
    f2.vitality = 0
    interactor._worm_handler.add_all([w])
    interactor._plant_handler.alga_handler.add_all([a])
    interactor._fish_handler.add_all([f1, f2])
    interactor._eat_at_spot(Position(1, 1))
    assert f1.vitality == 15 and f2.vitality == 15
