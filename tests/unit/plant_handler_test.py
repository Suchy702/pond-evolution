from unittest.mock import Mock

import pytest

from src.object.alga import Alga
from src.object.alga_maker import AlgaMaker
from src.object_handler.plant_handler import PlantHandler
from src.position import Position
# noinspection PyUnresolvedReferences
from tests.helper import settings


@pytest.fixture
def plant_handler(settings):
    return PlantHandler(settings)


def test_detach_algae_from_maker(plant_handler):
    maker = AlgaMaker(Position(0, 9), 10)
    maker.choose_algae_amount = Mock()
    maker.choose_algae_amount.return_value = 3
    plant_handler.alga_handler.add = Mock()

    plant_handler._detach_algae_from_maker(maker)
    assert plant_handler.alga_handler.add.call_count == 3


def test_get_spot_object(plant_handler):
    plant_handler.alga_handler.add(Alga(10, Position(0, 3), 5))
    plant_handler.alga_maker_handler.add(AlgaMaker(Position(0, 3), 5))
    assert len(plant_handler.get_spot_objects(Position(0, 3))) == 2
