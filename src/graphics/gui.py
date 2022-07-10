from math import ceil

import pygame
from pygame.surface import Surface

from src.constants import CELL_MIN_PX_SIZE, CELL_MAX_PX_SIZE
from src.events.event_emitter import EventEmitter
from src.graphics.image_handler.utility import get_object_image
from src.simulation_settings import SimulationSettings

VERBOSE = True


class GUI:
    def __init__(self, settings: SimulationSettings):
        self.settings: SimulationSettings = settings

        self._screen: Surface = pygame.display.set_mode([self.settings.screen_width, self.settings.screen_height])
        #self._screen: Surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.cell_size: int = CELL_MIN_PX_SIZE  # length of square cell in px
        self.x_offset: int = 0
        self.y_offset: int = 0
        self.center_view()

        self._event_emitter = EventEmitter()

    def draw_empty_frame(self) -> None:
        self._screen.fill((0, 0, 0))
        self.draw_boundary()

    # Get indices of cells that are fully visible
    def get_visible_grid_coordinates(self) -> tuple[int, int, int, int]:
        x_min = int(ceil(-self.x_offset / self.cell_size))
        x_max = (self.settings.screen_width - self.cell_size - self.x_offset) // self.cell_size

        y_min = int(ceil(-self.y_offset / self.cell_size))
        y_max = (self.settings.screen_height - self.cell_size - self.y_offset) // self.cell_size

        return x_min, x_max, y_min, y_max

    def draw_boundary(self):
        rect = pygame.Rect(
            self.x_offset, self.y_offset,
            self.settings.pond_width * self.cell_size, self.settings.pond_height * self.cell_size
        )
        pygame.draw.rect(self._screen, (138, 219, 239), rect, 0)

    def center_view(self) -> None:
        self.x_offset = self.settings.screen_width // 2 - self.settings.pond_width * self.cell_size // 2
        self.y_offset = self.settings.screen_height // 2 - self.settings.pond_height * self.cell_size // 2

    @staticmethod
    def _calc_left_half(x1, x2) -> float:
        middle = (x1 + x2) / 2
        return (middle - x1) / 2

    @staticmethod
    def _calc_top_half(y1, y2) -> float:
        middle = (y1 + y2) / 2
        return (middle - y1) / 2

    def zoom(self, change: int) -> None:
        old = self.cell_size
        self.cell_size = min(max(CELL_MIN_PX_SIZE, self.cell_size + change), CELL_MAX_PX_SIZE)

        if self.cell_size == old:
            return

        # try to zoom at point in the middle
        coor = self.get_visible_grid_coordinates()
        self.change_x_offset(int(-self._calc_left_half(coor[0], coor[1]) * change))
        self.change_y_offset(int(-self._calc_top_half(coor[2], coor[3]) * change))

    def is_animation_finished(self):
        return not self._event_emitter.is_animation_event()

    def change_y_offset(self, val) -> None:
        y_offset_limit = -(self.settings.pond_height * self.cell_size - self.settings.screen_height)

        if y_offset_limit < 0:
            self.y_offset = max(min(self.y_offset + val, 0), y_offset_limit)
        else:
            self.y_offset = max(min(self.y_offset + val, y_offset_limit), 0)

    def change_x_offset(self, val) -> None:
        x_offset_limit = -(self.settings.pond_width * self.cell_size - self.settings.screen_width)

        if x_offset_limit < 0:
            self.x_offset = max(min(self.x_offset + val, 0), x_offset_limit)
        else:
            self.x_offset = max(min(self.x_offset + val, x_offset_limit), 0)

    def draw_object(self, obj, x, y):
        rect = pygame.Rect(x, y, self.cell_size, self.cell_size)

        image = get_object_image(obj)
        self._screen.blit(pygame.transform.scale(image, (self.cell_size, self.cell_size)), rect)

