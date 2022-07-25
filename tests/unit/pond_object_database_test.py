import pytest

from src.pond.pond_object_database import PondObjectDatabase
# noinspection PyUnresolvedReferences
from tests.helper import pond_object, get_object


@pytest.fixture
def database():
    return PondObjectDatabase()


def test_add(pond_object, database):
    database.add(pond_object)
    assert database._object_database[pond_object.id] == pond_object


def test_adding_same_obj_twice(pond_object, database):
    database.add(pond_object)
    with pytest.raises(Exception):
        database.add(pond_object)


def test_remove(pond_object, database):
    database.add(pond_object)
    database.remove(pond_object)
    assert database.size == 0


def test_removing_obj_not_in_database(pond_object, database):
    with pytest.raises(Exception):
        database.remove(pond_object)


def test_id_counter_behaviour_when_adding(database):
    objects = [get_object(), get_object()]
    database.add(objects[0])
    database.add(objects[1])
    assert database._id_counter == 2


def test_id_counter_behaviour_when_removing(database):
    objects = [get_object(), get_object()]
    database.add(objects[0])
    database.add(objects[1])
    database.remove(objects[1])
    database.remove(objects[0])
    assert database._id_counter == 2
