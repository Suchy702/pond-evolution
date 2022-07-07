import pytest

from src.pond_object_database import PondObjectDatabase
from src.object.pond_object import PondObject
from src.position import Position


@pytest.fixture
def obj():
    return PondObject('T', Position(0, 0))


@pytest.fixture
def sample_base():
    return PondObjectDatabase()


def test_add(obj, sample_base):
    sample_base.add(obj)
    assert sample_base._object_database[obj.id] == obj


def test_adding_same_obj_twice(obj, sample_base):
    sample_base.add(obj)
    with pytest.raises(Exception):
        sample_base.add(obj)


def test_remove(obj, sample_base):
    sample_base.add(obj)
    sample_base.remove(obj)
    assert sample_base.size == 0


def test_removing_obj_which_not_in_base(obj, sample_base):
    with pytest.raises(Exception):
        sample_base.remove(obj)


def test_id_counter_behaviour_when_adding(sample_base):
    objects = [PondObject('T', Position(1, 1)), PondObject('F', Position(1, 1))]
    sample_base.add(objects[0])
    sample_base.add(objects[1])
    assert sample_base._id_counter == 2


def test_id_counter_behaviour_when_removing(sample_base):
    objects = [PondObject('T', Position(1, 1)), PondObject('F', Position(1, 1))]
    sample_base.add(objects[0])
    sample_base.add(objects[1])
    sample_base.remove(objects[1])
    sample_base.remove(objects[0])
    assert sample_base._id_counter == 2
