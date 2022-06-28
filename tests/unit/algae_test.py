import pytest
from src.algae import ALGAE_SURFACING_SPEED_DIV
from src.position import Position
from tests.unit.test_helper import get_obejct

@pytest.fixture
def alg():
    return get_obejct('A', pos=Position(10, 10), pond_dim=(50, 50))

def test_surfacing_speed_setting(alg):
    assert alg._surfacing_speed == max(1, 50 // ALGAE_SURFACING_SPEED_DIV)

def test_find_pos_to_move(alg):
    assert alg.find_pos_to_move() == Position(alg.pos.y-alg._surfacing_speed, alg.pos.x)