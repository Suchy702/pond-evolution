from math import ceil

import pygame
from pygame.surface import Surface

from src.constants import SCREEN_HEIGHT, SCREEN_WIDTH, POND_WIDTH, POND_HEIGHT
from src.object_handler.pond_object_handler import PondObjectHandler
from src.simulation_settings import SimulationSettings


class GUI:
    def __init__(self, settings: SimulationSettings, handlers: list[PondObjectHandler]):
        self._settings = settings
        self._handlers: list[PondObjectHandler] = handlers

        self._screen: Surface = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        self._cell_size: int = 50  # length of square cell in px
        self._x_offset = 100
        self._y_offset = 100

    def draw_frame(self):
        self._screen.fill((255, 255, 255))
        coor = self.get_visible_grid_coordinates()
        self.draw_full_squares(coor)
        self.draw_cut_squares(coor)
        pygame.display.flip()

    def get_visible_grid_coordinates(self):
        x_min = int(ceil(-self._x_offset / self._cell_size))
        x_max = (SCREEN_WIDTH - self._cell_size - self._x_offset) // self._cell_size

        y_min = int(ceil(-self._y_offset / self._cell_size))
        y_max = (SCREEN_HEIGHT - self._cell_size - self._y_offset) // self._cell_size

        assert x_min <= x_max
        assert y_min <= y_max

        # if x_min >= POND_WIDTH or x_max < 0 or x_min > x_max:
        #    return None

        # if y_min >= POND_HEIGHT or y_max < 0 or y_min > y_max:
        #    return None

        return x_min, x_max, y_min, y_max

    def draw_full_squares(self, coor):
        clipped_x = self.clip_x(coor[0], coor[1])
        clipped_y = self.clip_y(coor[2], coor[3])

        for i in range(clipped_x[0], clipped_x[1] + 1):
            for j in range(clipped_y[0], clipped_y[1] + 1):
                rect = pygame.Rect(i * self._cell_size + self._x_offset, j * self._cell_size + self._y_offset,
                                   self._cell_size, self._cell_size)
                pygame.draw.rect(self._screen, (0, 0, 0), rect, 1)

    def draw_cut_squares(self, coor):
        clipped_x = self.clip_x(coor[0], coor[1])
        clipped_y = self.clip_y(coor[2], coor[3])

        is_left_column_cut = (self._x_offset % self._cell_size != 0)
        is_right_column_cut = (SCREEN_WIDTH - ((clipped_x[1] + 1) * self._cell_size + self._x_offset) != 0)
        is_top_row_cut = (self._y_offset % self._cell_size != 0)
        is_bottom_row_cut = (SCREEN_HEIGHT - ((clipped_y[1] + 1) * self._cell_size + self._y_offset) != 0)

        # left column
        if coor[0] - 1 >= 0 and is_left_column_cut:
            for j in range(clipped_y[0], clipped_y[1] + 1):
                rect = pygame.Rect((coor[0] - 1) * self._cell_size + self._x_offset,
                                   j * self._cell_size + self._y_offset, self._cell_size, self._cell_size)
                pygame.draw.rect(self._screen, (0, 0, 0), rect, 1)

        # right column
        if coor[1] + 1 < POND_WIDTH and is_right_column_cut:
            for j in range(clipped_y[0], clipped_y[1] + 1):
                rect = pygame.Rect((coor[1] + 1) * self._cell_size + self._x_offset,
                                   j * self._cell_size + self._y_offset, self._cell_size, self._cell_size)
                pygame.draw.rect(self._screen, (0, 0, 0), rect, 1)

        # top row
        if coor[2] - 1 >= 0 and is_top_row_cut:
            for i in range(clipped_x[0], clipped_x[1] + 1):
                rect = pygame.Rect(i * self._cell_size + self._x_offset,
                                   (coor[2] - 1) * self._cell_size + self._y_offset, self._cell_size, self._cell_size)
                pygame.draw.rect(self._screen, (0, 0, 0), rect, 1)

        if coor[3] + 1 < POND_HEIGHT and is_bottom_row_cut:
            for i in range(clipped_x[0], clipped_x[1] + 1):
                rect = pygame.Rect(i * self._cell_size + self._x_offset,
                                   (coor[3] + 1) * self._cell_size + self._y_offset, self._cell_size, self._cell_size)
                pygame.draw.rect(self._screen, (0, 0, 0), rect, 1)

        # top-left cell
        if coor[0] - 1 >= 0 and coor[2] - 1 >= 0 and (is_top_row_cut or is_left_column_cut):
            rect = pygame.Rect((coor[0] - 1) * self._cell_size + self._x_offset,
                               (coor[2] - 1) * self._cell_size + self._y_offset,
                               self._cell_size, self._cell_size)
            pygame.draw.rect(self._screen, (0, 0, 0), rect, 1)

        # top-right cell
        if coor[1] + 1 < POND_WIDTH and coor[2] - 1 >= 0 and (
                is_top_row_cut or is_right_column_cut):
            rect = pygame.Rect((coor[1] + 1) * self._cell_size + self._x_offset,
                               (coor[2] - 1) * self._cell_size + self._y_offset,
                               self._cell_size, self._cell_size)
            pygame.draw.rect(self._screen, (0, 0, 0), rect, 1)

        # bottom-left cell
        if coor[0] - 1 >= 0 and coor[3] + 1 < POND_HEIGHT and (
                is_bottom_row_cut or is_left_column_cut):
            rect = pygame.Rect((coor[0] - 1) * self._cell_size + self._x_offset,
                               (coor[3] + 1) * self._cell_size + self._y_offset,
                               self._cell_size, self._cell_size)
            pygame.draw.rect(self._screen, (0, 0, 0), rect, 1)

        # bottom-right cell
        if coor[1] + 1 < POND_WIDTH and coor[3] + 1 < POND_HEIGHT and (
                is_bottom_row_cut or is_right_column_cut):
            rect = pygame.Rect((coor[1] + 1) * self._cell_size + self._x_offset,
                               (coor[3] + 1) * self._cell_size + self._y_offset,
                               self._cell_size, self._cell_size)
            pygame.draw.rect(self._screen, (0, 0, 0), rect, 1)

    def clip_x(self, min_x, max_x):
        return max(min_x, 0), min(max_x, POND_WIDTH - 1)

    def clip_y(self, min_y, max_y):
        return max(min_y, 0), min(max_y, POND_HEIGHT - 1)
