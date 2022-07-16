from unittest.mock import Mock

import pytest

from src.object.alga_maker import AlgaMaker
from src.object_handler.alga_maker_handler import AlgaMakerHandler
from src.position import Position
# noinspection PyUnresolvedReferences
from tests.helper import settings


@pytest.fixture
def alga_maker_handler(settings):
    return AlgaMakerHandler(settings)


def test_create_algae(alga_maker_handler):
    alga_maker = AlgaMaker(Position(0, 4), 5)
    alga_maker.choose_algae_amount = Mock()
    alga_maker.choose_algae_amount.return_value = 3
    assert len(alga_maker_handler.create_algae(alga_maker)) == 3
