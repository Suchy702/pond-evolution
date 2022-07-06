import pytest

from src.worm_handler import WormHandler
from tests.unit.helper_with_testing import get_object
from src.position import Position


@pytest.fixture
def sample_worm_h():
    return WormHandler(5, 10)


def test_del_worms_from_the_ground(sample_worm_h):
    w1 = get_object('W', pos=Position(4, 5))
    w2 = get_object('W', pos=Position(0, 2))
    w3 = get_object('W', pos=Position(4, 2))
    w33 = get_object('W', pos=Position(4, 2))
    sample_worm_h.add_all([w1, w2, w3, w33])
    sample_worm_h.del_worms_from_the_ground()
    assert sample_worm_h._base.size == 1
