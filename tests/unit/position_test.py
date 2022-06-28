import pytest
from src.position import Position


@pytest.fixture
def pos_0_0():
    return Position(0, 0)


@pytest.mark.parametrize("change,expected", [([0, 0], [0, 0]), ([1, 2], [1, 2]), ([-3, 4], [-3, 4])])
def test_changed(pos_0_0, change, expected):
    new_pos = pos_0_0.changed(change[0], change[1])
    assert new_pos.y == expected[0] and new_pos.x == expected[1]
