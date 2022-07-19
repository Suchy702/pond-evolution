import os
from unittest.mock import patch, Mock

import pygame
import pytest

from src.game import Game

os.environ["SDL_VIDEODRIVER"] = "dummy"

cwd = os.getcwd()
move_to_parent = 0

while os.path.basename(cwd) != 'pond-evolution':
    move_to_parent += 1
    cwd = os.path.dirname(cwd)

IMG_DIR_PATH = os.path.join(*(['..'] * move_to_parent), 'resources', 'object_images')


class SimulationSettingsMock:
    screen_pond_height = 640
    screen_pond_width = 1080
    pond_height = 32
    pond_width = 54
    screen_height = 720
    screen_width = 1080
    get_user_settings = Mock()


@patch('pygame.event.get')
@patch('src.game.SimulationSettings', new=SimulationSettingsMock)
@patch('src.graphics.image_handler.image_handler.IMG_DIR_PATH', IMG_DIR_PATH)
@pytest.mark.timeout(30)
def test_game(event_get_mock):
    events: list[any] = [[Mock()]] * 100 + [[pygame.event.Event(pygame.locals.QUIT)]]
    event_get_mock.side_effect = events

    game = Game()
    game.run()

    assert SimulationSettingsMock.get_user_settings.call_count == 1
    assert event_get_mock.call_count == 101
