import pytest

from src.pond import Pond
from src.position import Position

from tests.unit.helper_with_testing import get_object

INF = 1_000_000_000


@pytest.fixture
def sample_pond():
    return Pond(5, 10)


@pytest.fixture
def obj():
    return get_object()


def test_add(sample_pond, obj):
    sample_pond.add(obj)
    assert obj in sample_pond.get_spot(obj.pos)


def test_adding_same_obj_twice(sample_pond, obj):
    sample_pond.add(obj)
    with pytest.raises(Exception):
        sample_pond.add(obj)


def test_remove(sample_pond, obj):
    sample_pond.add(obj)
    sample_pond.remove(obj)
    assert len(sample_pond.get_spot(obj.pos)) == 0


def test_removing_object_which_not_in_spot(sample_pond, obj):
    with pytest.raises(Exception):
        sample_pond.remove(obj)


@pytest.mark.parametrize("pos", (Position(-1, -1), Position(INF, INF), Position(0, 0), Position(1, 1)))
def test_correct_pos(sample_pond, pos):
    corr_pos = sample_pond.correct_pos(pos)
    assert 0 <= corr_pos.y < sample_pond.height and 0 <= corr_pos.x < sample_pond.width


@pytest.mark.parametrize("pos", (Position(4, 1), Position(4, 0), Position(4, 3)))
def test_is_on_the_ground_when_is_on_the_ground(sample_pond, pos):
    assert sample_pond.is_on_the_ground(pos) is True


@pytest.mark.parametrize("pos", (Position(0, 0), Position(1, 1), Position(2, 0)))
def test_is_on_the_gound_when_not_on_the_ground(sample_pond, pos):
    assert sample_pond.is_on_the_ground(pos) is False


@pytest.mark.parametrize("pos", (Position(0, 0), Position(1, 1), Position(0, 4)))
def test_is_on_surface(sample_pond, pos):
    assert sample_pond.is_on_surface(pos) == (pos.y == 0)
