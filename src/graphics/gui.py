from math import ceil, copysign

import pygame
from pygame.surface import Surface

from src.constants import CELL_MIN_PX_SIZE, CELL_MAX_PX_SIZE, BLACK, LIGHT_BLUE, GRAY
from src.events.event_emitter import EventEmitter
from src.graphics.image_handler.utility import get_object_image
from src.simulation_settings import SimulationSettings


def clip(val: int, a: int, b: int) -> int:
    # Clips `val` to range [min(a, b), max(a, b)]
    if a > b:
        a, b = b, a
    return min(max(val, a), b)


class GUI:
    def __init__(self, settings: SimulationSettings):
        self.settings: SimulationSettings = settings

        self._screen: Surface = pygame.display.set_mode([self.settings.screen_width, self.settings.screen_height])
        self._cell_size: int = CELL_MIN_PX_SIZE  # length of cell's side in px. Cell is a square
        self._x_offset: int = 0
        self._y_offset: int = 0
        self.center_view()

        self._event_emitter = EventEmitter()

    @property
    def x_offset(self) -> int:
        return self._x_offset

    @x_offset.setter
    def x_offset(self, val: int) -> None:
        x_offset_limit = -(self.settings.pond_width * self._cell_size - self.settings.screen_pond_width)
        self._x_offset = clip(val, 0, x_offset_limit)

    @property
    def y_offset(self) -> int:
        return self._y_offset

    @y_offset.setter
    def y_offset(self, val: int) -> None:
        y_offset_limit = -(self.settings.pond_height * self._cell_size - self.settings.screen_pond_height)
        self._y_offset = clip(val, 0, y_offset_limit)

    @property
    def cell_size(self) -> int:
        return self._cell_size

    @cell_size.setter
    def cell_size(self, val: int) -> None:
        self._cell_size = min(max(CELL_MIN_PX_SIZE, val), CELL_MAX_PX_SIZE)

    def draw_empty_frame(self) -> None:
        self._screen.fill(BLACK)
        self.draw_pond_area()

    def get_visible_gird_x_coordinates(self) -> tuple[int, int]:
        x_min = int(ceil(-self._x_offset / self._cell_size))
        x_max = (self.settings.screen_pond_width - self._cell_size - self._x_offset) // self._cell_size
        return x_min, x_max

    def get_visible_grid_y_coordinates(self) -> tuple[int, int]:
        y_min = int(ceil(-self._y_offset / self._cell_size))
        y_max = (self.settings.screen_pond_height - self._cell_size - self._y_offset) // self._cell_size
        return y_min, y_max

    def get_visible_grid_coordinates(self) -> tuple[int, int, int, int]:
        x_min, x_max = self.get_visible_gird_x_coordinates()
        y_min, y_max = self.get_visible_grid_y_coordinates()
        return x_min, x_max, y_min, y_max

    def draw_pond_area(self):
        rect_width, rect_height = self.settings.pond_width * self._cell_size, self.settings.pond_height * self._cell_size
        rect = pygame.Rect(self._x_offset, self._y_offset, rect_width, rect_height)
        pygame.draw.rect(self._screen, LIGHT_BLUE, rect, 0)

    def draw_ui(self):
        rect = pygame.Rect(0, self.settings.screen_pond_height, self.settings.screen_width,
                           self.settings.screen_height - self.settings.screen_pond_height)
        pygame.draw.rect(self._screen, GRAY, rect, 0)

    def center_view(self) -> None:
        self.x_offset = int(self.settings.screen_pond_width / 2 - self.settings.pond_width * self._cell_size / 2)
        self.y_offset = int(self.settings.screen_pond_height / 2 - self.settings.pond_height * self._cell_size / 2)

    def zoom(self, change: int) -> None:
        old_cell_size = self._cell_size
        self.cell_size += change

        if self._cell_size == old_cell_size:
            return

        """
        The idea is to find distance between point in the middle of the screen and point in the middle ozond and
        then inspect how this distance changes upon cell_size change
        """

        pond_center_x: float = self._x_offset + old_cell_size * self.settings.pond_width // 2
        pond_center_y: float = self._y_offset + old_cell_size * self.settings.pond_height // 2

        if self.settings.pond_width % 2 == 1:
            pond_center_x += old_cell_size / 2

        if self.settings.pond_height % 2 == 1:
            pond_center_y += old_cell_size / 2

        screen_center_x = self.settings.screen_pond_width / 2
        screen_center_y = self.settings.screen_pond_height / 2

        vertical_cells = min(
            abs(screen_center_x - pond_center_x) / old_cell_size,
            self.settings.pond_width / 2
        ) * copysign(1, screen_center_x - pond_center_x)
        horizontal_cells = min(
            abs(screen_center_y - pond_center_y) / old_cell_size,
            self.settings.screen_pond_height / 2
        ) * copysign(1, screen_center_y - pond_center_y)

        diff_x = screen_center_x - pond_center_x
        diff_y = screen_center_y - pond_center_y

        diff_x_after_zoom = diff_x + vertical_cells * change
        diff_y_after_zoom = diff_y + horizontal_cells * change

        # pond center after zoom
        pond_center_x = self._x_offset + self._cell_size * self.settings.pond_width // 2
        pond_center_y = self._y_offset + self._cell_size * self.settings.pond_height // 2

        # point to which current screen center is transformed after zoom
        old_screen_center_x = pond_center_x + diff_x_after_zoom
        old_screen_center_y = pond_center_y + diff_y_after_zoom

        self.x_offset += int(screen_center_x - old_screen_center_x)
        self.y_offset += int(screen_center_y - old_screen_center_y)

    def is_animation_finished(self):
        return not self._event_emitter.is_animation_event_present()

    def draw_object(self, obj, x, y):
        rect = pygame.Rect(x, y, self._cell_size, self._cell_size)
        image = get_object_image(obj)
        self._screen.blit(pygame.transform.scale(image, (self._cell_size, self._cell_size)), rect)
