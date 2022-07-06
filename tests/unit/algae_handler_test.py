import pytest

from src.algae_handler import AlgaeHandler
from tests.unit.helper_with_testing import get_object
from src.position import Position


@pytest.fixture
def sample_alg_h():
    return AlgaeHandler(5, 10)


def test_del_algs_on_surface(sample_alg_h):
    a1 = get_object('A', pos=Position(0, 1))
    a2 = get_object('A', pos=Position(2, 3))
    a3 = get_object('A', pos=Position(0, 2))
    a33 = get_object('A', pos=Position(0, 2))
    sample_alg_h.add_all([a1, a2, a3, a33])
    sample_alg_h.del_algs_on_surface()
    assert sample_alg_h._base.size == 1
