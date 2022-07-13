from math import ceil

import pygame
from pygame.surface import Surface

from src.constants import CELL_MIN_PX_SIZE, CELL_MAX_PX_SIZE, BLACK, LIGHT_BLUE, GRAY
from src.events.event_emitter import EventEmitter
from src.graphics.image_handler.utility import get_object_image
from src.simulation_settings import SimulationSettings

VERBOSE = True

def signum(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    return 0

class GUI:
    def __init__(self, settings: SimulationSettings):
        self.settings: SimulationSettings = settings

        self._screen: Surface = pygame.display.set_mode([self.settings.screen_width, self.settings.screen_height])
        # self._screen: Surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.cell_size: int = CELL_MIN_PX_SIZE  # length of square cell in px
        self.x_offset: int = 0
        self.y_offset: int = 0
        self.center_view()

        self._event_emitter = EventEmitter()

    def draw_empty_frame(self) -> None:
        self._screen.fill(BLACK)
        self.draw_boundary()

    def get_visible_gird_x_coordinates(self) -> tuple[int, int]:
        x_min = int(ceil(-self.x_offset / self.cell_size))
        x_max = (self.settings.screen_pond_width - self.cell_size - self.x_offset) // self.cell_size
        return x_min, x_max

    def get_visible_grid_y_coordinates(self) -> tuple[int, int]:
        y_min = int(ceil(-self.y_offset / self.cell_size))
        y_max = (self.settings.screen_pond_height - self.cell_size - self.y_offset) // self.cell_size
        return y_min, y_max

    def get_visible_grid_coordinates(self) -> tuple[int, int, int, int]:
        x_min, x_max = self.get_visible_gird_x_coordinates()
        y_min, y_max = self.get_visible_grid_y_coordinates()
        return x_min, x_max, y_min, y_max

    def draw_boundary(self):
        rect_width, rect_height = self.settings.pond_width * self.cell_size, self.settings.pond_height * self.cell_size
        rect = pygame.Rect(self.x_offset, self.y_offset, rect_width, rect_height)
        pygame.draw.rect(self._screen, LIGHT_BLUE, rect, 0)

    def draw_ui(self):
        rect = pygame.Rect(0, self.settings.screen_pond_height, self.settings.screen_width,
                           self.settings.screen_height - self.settings.screen_pond_height)
        pygame.draw.rect(self._screen, GRAY, rect, 0)

    def center_view(self) -> None:
        self.x_offset = self.settings.screen_pond_width // 2 - self.settings.pond_width * self.cell_size // 2
        self.y_offset = self.settings.screen_pond_height // 2 - self.settings.pond_height * self.cell_size // 2

    def zoom(self, change: int) -> None:
        old_cell_size = self.cell_size
        self.cell_size = min(max(CELL_MIN_PX_SIZE, self.cell_size + change), CELL_MAX_PX_SIZE)

        if self.cell_size == old_cell_size:
            return

        """
        The idea is to find distance between point in the middle of the screen and point in the middle of the pond and
        then inspect how this distance changes upon cell_size change
        """

        pond_center_x: float = self.x_offset + old_cell_size * self.settings.pond_width // 2
        pond_center_y: float = self.y_offset + old_cell_size * self.settings.pond_height // 2

        if self.settings.pond_width % 2 == 1:
            pond_center_x += old_cell_size / 2

        if self.settings.pond_height % 2 == 1:
            pond_center_y += old_cell_size / 2

        screen_center_x = self.settings.screen_pond_width / 2
        screen_center_y = self.settings.screen_pond_height / 2

        vertical_cells = min(abs(screen_center_x - pond_center_x) / old_cell_size,
                             self.settings.pond_width / 2) * signum(screen_center_x - pond_center_x)
        horizontal_cells = min(abs(screen_center_y - pond_center_y) / old_cell_size,
                               self.settings.screen_pond_height / 2) * signum(screen_center_y - pond_center_y)

        diff_x = self.settings.screen_pond_width / 2 - pond_center_x
        diff_y = self.settings.screen_pond_height / 2 - pond_center_y

        diff_x_after_zoom = diff_x + vertical_cells * change
        diff_y_after_zoom = diff_y + horizontal_cells * change

        pond_center_x = self.x_offset + self.cell_size * self.settings.pond_width // 2
        pond_center_y = self.y_offset + self.cell_size * self.settings.pond_height // 2

        old_screen_center_x = pond_center_x + diff_x_after_zoom
        old_screen_center_y = pond_center_y + diff_y_after_zoom

        self.change_x_offset(int(screen_center_x - old_screen_center_x))
        self.change_y_offset(int(screen_center_y - old_screen_center_y))

    def is_animation_finished(self):
        return not self._event_emitter.is_animation_event()

    def change_y_offset(self, val) -> None:
        y_offset_limit = -(self.settings.pond_height * self.cell_size - self.settings.screen_pond_height)

        if y_offset_limit < 0:
            self.y_offset = max(min(self.y_offset + val, 0), y_offset_limit)
        else:
            self.y_offset = max(min(self.y_offset + val, y_offset_limit), 0)

    def change_x_offset(self, val) -> None:
        x_offset_limit = -(self.settings.pond_width * self.cell_size - self.settings.screen_pond_width)

        if x_offset_limit < 0:
            self.x_offset = max(min(self.x_offset + val, 0), x_offset_limit)
        else:
            self.x_offset = max(min(self.x_offset + val, x_offset_limit), 0)

    def draw_object(self, obj, x, y):
        rect = pygame.Rect(x, y, self.cell_size, self.cell_size)

        image = get_object_image(obj)
        self._screen.blit(pygame.transform.scale(image, (self.cell_size, self.cell_size)), rect)
