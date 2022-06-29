import pytest

from src.pond_object import PondObject
from src.position import Position


def test_set_id_when_already_set():
    obj = PondObject('T', Position(0, 0))
    obj.id = 3
    with pytest.raises(Exception):
        obj.id = 2
