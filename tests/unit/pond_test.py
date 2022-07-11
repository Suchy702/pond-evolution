import pytest

from src.pond import Pond
from src.position import Position
# noinspection PyUnresolvedReferences
from tests.helper import pond_object, INF, settings


@pytest.fixture
def pond(settings):
    return Pond(settings)


def test_add(pond, pond_object):
    pond.add(pond_object)
    assert pond_object in pond.get_spot(pond_object.pos)


def test_adding_same_obj_twice(pond, pond_object):
    pond.add(pond_object)
    with pytest.raises(Exception):
        pond.add(pond_object)


def test_remove(pond, pond_object):
    pond.add(pond_object)
    pond.remove(pond_object)
    assert len(pond.get_spot(pond_object.pos)) == 0


def test_removing_object_not_in_spot(pond, pond_object):
    with pytest.raises(Exception):
        pond.remove(pond_object)


@pytest.mark.parametrize("pos", (Position(-1, -1), Position(INF, INF), Position(0, 0), Position(1, 1)))
def test_trim_position(pond, pos):
    corr_pos = pond.trim_position(pos)
    assert 0 <= corr_pos.y < pond.height and 0 <= corr_pos.x < pond.width


@pytest.mark.parametrize("pos", (Position(4, 1), Position(4, 0), Position(4, 3)))
def test_is_on_ground_when_is_on_ground(pond, pos):
    assert pond.is_on_ground(pos) is True


@pytest.mark.parametrize("pos", (Position(0, 0), Position(1, 1), Position(2, 0)))
def test_is_on_ground_when_not_on_ground(pond, pos):
    assert pond.is_on_ground(pos) is False


@pytest.mark.parametrize("pos", (Position(0, 0), Position(1, 1), Position(0, 4)))
def test_is_on_surface(pond, pos):
    assert pond.is_on_surface(pos) == (pos.y == 0)
