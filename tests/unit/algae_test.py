import pytest

from src.constants import ALGA_SURFACING_STEPS
from src.object_kind import ObjectKind
from src.position import Position
from tests.unit.helper import get_object


@pytest.fixture
def alga():
    return get_object(ObjectKind.ALGA, pos=Position(10, 10), pond_dim=(50, 50))


def test_surfacing_speed_setting(alga):
    assert alga._surfacing_speed == max(1, 50 // ALGA_SURFACING_STEPS)


def test_find_pos_to_move(alga):
    assert alga.find_pos_to_move() == Position(alga.pos.y - alga._surfacing_speed, alga.pos.x)