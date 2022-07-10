from math import ceil

import pygame
from pygame.surface import Surface

from src.events.event_emitter import EventEmitter
from src.graphics.image_handler.utility import get_object_image
from src.simulation_settings import SimulationSettings

VERBOSE = True


class GUI:
    def __init__(self, settings: SimulationSettings):
        self.settings: SimulationSettings = settings

        self._screen: Surface = pygame.display.set_mode([self.settings.screen_width, self.settings.screen_height])
        self.cell_size: int = 20  # length of square cell in px
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
        pygame.draw.rect(self._screen, (255, 255, 255), rect, 0)

    def clip_x(self, min_x, max_x) -> tuple[int, int]:
        return max(min_x, 0), min(max_x, self.settings.pond_width - 1)

    def clip_y(self, min_y, max_y) -> tuple[int, int]:
        return max(min_y, 0), min(max_y, self.settings.pond_height - 1)

    def center_view(self) -> None:
        self.x_offset = self.settings.screen_width // 2 - self.settings.pond_width * self.cell_size // 2
        self.y_offset = self.settings.screen_height // 2 - self.settings.pond_height * self.cell_size // 2

    def zoom(self, change: int) -> None:
        old = self.cell_size
        self.cell_size = min(max(10, self.cell_size + change), 100)

        if self.cell_size == old:
            return

        # try to zoom at point in the middle
        coor = self.get_visible_grid_coordinates()
        middle = (coor[1] + coor[0]) / 2
        left_half = (max(middle, 0) - max(coor[0], 0)) / 2
        middle = (coor[3] + coor[2]) / 2
        top_half = (max(middle, 0) - max(coor[2], 0)) / 2
        self.x_offset = int(self.x_offset - left_half * change)
        self.y_offset = int(self.y_offset - top_half * change)

    def is_animation_finished(self):
        return not self._event_emitter.is_animation_event()

    def draw_object(self, obj, x, y):
        # TODO: teraz mozemy rysowac obrazki o dowolnym ration, wiec mozna zmienic self._cell_size na co innego
        rect = pygame.Rect(x, y, self.cell_size, self.cell_size)

        image = get_object_image(obj)
        self._screen.blit(pygame.transform.scale(image, (self.cell_size, self.cell_size)), rect)
