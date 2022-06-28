import pytest

from src.pond import Pond
from tests.unit.helper_with_testing import get_object

@pytest.fixture
def sample_pond():
    return Pond(5, 10)

@pytest.fixture
def obj():
    return get_object()

def test_add(sample_pond, obj):
    sample_pond.add(obj)
    assert obj in sample_pond.get_spot(obj.pos)

def test_adding_twice_same_obj(sample_pond, obj):
    sample_pond.add(obj)
    with pytest.raises(Exception):
        sample_pond.add(obj)

def test_

