import pytest

from src.object.object_kind import ObjectKind
from src.object_handler.worm_handler import WormHandler
from src.position import Position
# noinspection PyUnresolvedReferences
from tests.helper import get_object, settings


@pytest.fixture
def worm_handler(settings):
    return WormHandler(settings)


def test_kill_worms_on_ground(worm_handler):
    w1 = get_object(ObjectKind.WORM, pos=Position(4, 4))
    w2 = get_object(ObjectKind.WORM, pos=Position(0, 2))
    w3 = get_object(ObjectKind.WORM, pos=Position(4, 2))
    w4 = get_object(ObjectKind.WORM, pos=Position(4, 2))

    worm_handler.add_all([w1, w2, w3, w4])
    worm_handler.remove_worms_on_the_ground()

    assert worm_handler._object_database.size == 1
