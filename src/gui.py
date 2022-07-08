from math import ceil

import pygame
from pygame.surface import Surface

from src.object_handler.pond_object_handler import PondObjectHandler
from src.simulation_settings import SimulationSettings


class GUI:
    def __init__(self, settings: SimulationSettings, handlers: list[PondObjectHandler]):
        self._settings: SimulationSettings = settings
        self._handlers: list[PondObjectHandler] = handlers

        self._screen: Surface = pygame.display.set_mode([self._settings.screen_width, self._settings.screen_height])
        self._cell_size: int = 50  # length of square cell in px
        self.x_offset: int = 100
        self.y_offset: int = 100

    @property
    def cell_size(self):
        return self._cell_size

    @cell_size.setter
    def cell_size(self, val):
        self._cell_size = min(max(10, val), 100)

    def draw_frame(self):
        self._screen.fill((255, 255, 255))
        self.draw_squares()
        pygame.display.flip()

    # Get indices of cells that are fully visible
    def get_visible_grid_coordinates(self):
        x_min = int(ceil(-self.x_offset / self._cell_size))
        x_max = (self._settings.screen_width - self._cell_size - self.x_offset) // self._cell_size

        y_min = int(ceil(-self.y_offset / self._cell_size))
        y_max = (self._settings.screen_height - self._cell_size - self.y_offset) // self._cell_size

        return x_min, x_max, y_min, y_max

    def draw_squares(self):
        visible_coordinates = self.get_visible_grid_coordinates()
        self.draw_full_squares(visible_coordinates)
        self.draw_cut_squares(visible_coordinates)

    def draw_full_squares(self, coor):
        clipped_x = self.clip_x(coor[0], coor[1])
        clipped_y = self.clip_y(coor[2], coor[3])

        for i in range(clipped_x[0], clipped_x[1] + 1):
            for j in range(clipped_y[0], clipped_y[1] + 1):
                rect = pygame.Rect(i * self._cell_size + self.x_offset, j * self._cell_size + self.y_offset,
                                   self._cell_size, self._cell_size)
                pygame.draw.rect(self._screen, (0, 0, 0), rect, 1)

    def draw_cut_squares(self, coor):
        clipped_x = self.clip_x(coor[0], coor[1])
        clipped_y = self.clip_y(coor[2], coor[3])

        is_left_column_cut = (self.x_offset % self._cell_size != 0)
        is_right_column_cut = (
                    self._settings.screen_width - ((clipped_x[1] + 1) * self._cell_size + self.x_offset) != 0)
        is_top_row_cut = (self.y_offset % self._cell_size != 0)
        is_bottom_row_cut = (self._settings.screen_height - ((clipped_y[1] + 1) * self._cell_size + self.y_offset) != 0)

        is_left_column_in_pond = (0 <= coor[0] - 1 < self._settings.pond_width)
        is_right_column_in_pond = (0 <= coor[1] + 1 < self._settings.pond_width)
        is_top_row_in_pond = (0 <= coor[2] - 1 < self._settings.pond_height)
        is_bottom_row_in_pond = (0 <= coor[3] + 1 < self._settings.pond_height)

        # left column
        if is_left_column_in_pond and is_left_column_cut:
            for j in range(clipped_y[0], clipped_y[1] + 1):
                rect = pygame.Rect(
                    (coor[0] - 1) * self._cell_size + self.x_offset, j * self._cell_size + self.y_offset,
                    self._cell_size, self._cell_size
                )
                pygame.draw.rect(self._screen, (0, 0, 0), rect, 1)

        # right column
        if is_right_column_in_pond and is_right_column_cut:
            for j in range(clipped_y[0], clipped_y[1] + 1):
                rect = pygame.Rect(
                    (coor[1] + 1) * self._cell_size + self.x_offset, j * self._cell_size + self.y_offset,
                    self._cell_size, self._cell_size
                )
                pygame.draw.rect(self._screen, (0, 0, 0), rect, 1)

        # top row
        if is_top_row_in_pond and is_top_row_cut:
            for i in range(clipped_x[0], clipped_x[1] + 1):
                rect = pygame.Rect(
                    i * self._cell_size + self.x_offset, (coor[2] - 1) * self._cell_size + self.y_offset,
                    self._cell_size, self._cell_size
                )
                pygame.draw.rect(self._screen, (0, 0, 0), rect, 1)

        # bottom row
        if is_bottom_row_in_pond and is_bottom_row_cut:
            for i in range(clipped_x[0], clipped_x[1] + 1):
                rect = pygame.Rect(
                    i * self._cell_size + self.x_offset, (coor[3] + 1) * self._cell_size + self.y_offset,
                    self._cell_size, self._cell_size
                )
                pygame.draw.rect(self._screen, (0, 0, 0), rect, 1)

        # top-left cell
        if is_top_row_in_pond and is_left_column_in_pond and (is_top_row_cut or is_left_column_cut):
            rect = pygame.Rect(
                (coor[0] - 1) * self._cell_size + self.x_offset, (coor[2] - 1) * self._cell_size + self.y_offset,
                self._cell_size, self._cell_size
            )
            pygame.draw.rect(self._screen, (0, 0, 0), rect, 1)

        # top-right cell
        if is_top_row_in_pond and is_right_column_in_pond and (is_top_row_cut or is_right_column_cut):
            rect = pygame.Rect(
                (coor[1] + 1) * self._cell_size + self.x_offset, (coor[2] - 1) * self._cell_size + self.y_offset,
                self._cell_size, self._cell_size
            )
            pygame.draw.rect(self._screen, (0, 0, 0), rect, 1)

        # bottom-left cell
        if is_bottom_row_in_pond and is_left_column_in_pond and (is_bottom_row_cut or is_left_column_cut):
            rect = pygame.Rect(
                (coor[0] - 1) * self._cell_size + self.x_offset, (coor[3] + 1) * self._cell_size + self.y_offset,
                self._cell_size, self._cell_size
            )
            pygame.draw.rect(self._screen, (0, 0, 0), rect, 1)

        # bottom-right cell
        if is_bottom_row_in_pond and is_right_column_in_pond and coor[3] + 1 < self._settings.pond_height and (
                is_bottom_row_cut or is_right_column_cut):
            rect = pygame.Rect(
                (coor[1] + 1) * self._cell_size + self.x_offset, (coor[3] + 1) * self._cell_size + self.y_offset,
                self._cell_size, self._cell_size
            )
            pygame.draw.rect(self._screen, (0, 0, 0), rect, 1)

    def clip_x(self, min_x, max_x):
        return max(min_x, 0), min(max_x, self._settings.pond_width - 1)

    def clip_y(self, min_y, max_y):
        return max(min_y, 0), min(max_y, self._settings.pond_height - 1)
