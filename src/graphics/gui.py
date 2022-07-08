import random
from math import ceil

import pygame
from pygame.surface import Surface

from src.events.event import Event, EventType
from src.events.event_handler import EventHandler
from src.events.event_manager import EventManager
from src.graphics.image_handler.image_handler import ImageHandler
from src.graphics.image_handler.utility import get_image_handlers
from src.object_handler.pond_object_handler import PondObjectHandler
from src.position import Position
from src.simulation_settings import SimulationSettings

VERBOSE = True


class GUI(EventHandler):
    def __init__(self, settings: SimulationSettings, handlers: list[PondObjectHandler]):
        self._settings: SimulationSettings = settings
        self._image_handlers: list[ImageHandler] = get_image_handlers(handlers)

        self._screen: Surface = pygame.display.set_mode([self._settings.screen_width, self._settings.screen_height])
        self._cell_size: int = 20  # length of square cell in px
        self._x_offset: int = 0
        self._y_offset: int = 0
        self._center_view()

        self._event_handler = EventManager()

    def draw_frame(self) -> None:
        self._screen.fill((255, 255, 255))
        self.draw_squares(True)
        pygame.display.flip()

    def draw_squares(self, show_grid=False) -> None:
        visible_coordinates = self.get_visible_grid_coordinates()
        self.draw_full_squares(visible_coordinates, show_grid)
        self.draw_cut_squares(visible_coordinates, show_grid)

    # Get indices of cells that are fully visible
    def get_visible_grid_coordinates(self) -> tuple[int, int, int, int]:
        x_min = int(ceil(-self._x_offset / self._cell_size))
        x_max = (self._settings.screen_width - self._cell_size - self._x_offset) // self._cell_size

        y_min = int(ceil(-self._y_offset / self._cell_size))
        y_max = (self._settings.screen_height - self._cell_size - self._y_offset) // self._cell_size

        return x_min, x_max, y_min, y_max

    def draw_full_squares(self, coor, show_grid=False) -> None:
        clipped_x = self.clip_x(coor[0], coor[1])
        clipped_y = self.clip_y(coor[2], coor[3])

        for i in range(clipped_x[0], clipped_x[1] + 1):
            for j in range(clipped_y[0], clipped_y[1] + 1):
                self._draw_images(i, j, show_grid)

    def draw_cut_squares(self, coor, show_grid=False) -> None:
        clipped_x = self.clip_x(coor[0], coor[1])
        clipped_y = self.clip_y(coor[2], coor[3])

        is_left_column_cut = (self._x_offset % self._cell_size != 0)
        is_right_column_cut = (
                self._settings.screen_width - ((clipped_x[1] + 1) * self._cell_size + self._x_offset) != 0)
        is_top_row_cut = (self._y_offset % self._cell_size != 0)
        is_bottom_row_cut = (
                    self._settings.screen_height - ((clipped_y[1] + 1) * self._cell_size + self._y_offset) != 0)

        is_left_column_in_pond = (0 <= coor[0] - 1 < self._settings.pond_width)
        is_right_column_in_pond = (0 <= coor[1] + 1 < self._settings.pond_width)
        is_top_row_in_pond = (0 <= coor[2] - 1 < self._settings.pond_height)
        is_bottom_row_in_pond = (0 <= coor[3] + 1 < self._settings.pond_height)

        # left column
        if is_left_column_in_pond and is_left_column_cut:
            for j in range(clipped_y[0], clipped_y[1] + 1):
                self._draw_images((coor[0] - 1), j, show_grid)

        # right column
        if is_right_column_in_pond and is_right_column_cut:
            for j in range(clipped_y[0], clipped_y[1] + 1):
                self._draw_images(coor[1] + 1, j, show_grid)

        # top row
        if is_top_row_in_pond and is_top_row_cut:
            for i in range(clipped_x[0], clipped_x[1] + 1):
                self._draw_images(i, coor[2] - 1, show_grid)

        # bottom row
        if is_bottom_row_in_pond and is_bottom_row_cut:
            for i in range(clipped_x[0], clipped_x[1] + 1):
                self._draw_images(i, coor[3] + 1, show_grid)

        # top-left cell
        if is_top_row_in_pond and is_left_column_in_pond and (is_top_row_cut or is_left_column_cut):
            self._draw_images(coor[0] - 1, coor[2] - 1, show_grid)

        # top-right cell
        if is_top_row_in_pond and is_right_column_in_pond and (is_top_row_cut or is_right_column_cut):
            self._draw_images(coor[1] + 1, coor[2] - 1)

        # bottom-left cell
        if is_bottom_row_in_pond and is_left_column_in_pond and (is_bottom_row_cut or is_left_column_cut):
            self._draw_images(coor[0] - 1, coor[3] + 1, show_grid)

        # bottom-right cell
        if is_bottom_row_in_pond and is_right_column_in_pond and coor[3] + 1 < self._settings.pond_height and (
                is_bottom_row_cut or is_right_column_cut):
            self._draw_images(coor[1] + 1, coor[3] + 1, show_grid)

    def clip_x(self, min_x, max_x) -> tuple[int, int]:
        return max(min_x, 0), min(max_x, self._settings.pond_width - 1)

    def clip_y(self, min_y, max_y) -> tuple[int, int]:
        return max(min_y, 0), min(max_y, self._settings.pond_height - 1)

    def _get_images(self, x, y) -> list[Surface]:
        images = []
        for img_handler in self._image_handlers:
            pos = Position(y, x)
            for img in img_handler.get_images_at_spot(pos):
                images.append(pygame.transform.scale(img, (self._cell_size, self._cell_size)))

        random.shuffle(images)
        return images

    def _draw_images(self, x, y, show_grid=False) -> None:
        rect = pygame.Rect(
            x * self._cell_size + self._x_offset, y * self._cell_size + self._y_offset,
            self._cell_size, self._cell_size
        )

        if show_grid:
            pygame.draw.rect(self._screen, (0, 0, 0), rect, 1)

        for image in self._get_images(x, y):
            self._screen.blit(image, rect)

    def _center_view(self) -> None:
        self._x_offset = self._settings.screen_width // 2 - self._settings.pond_width * self._cell_size // 2
        self._y_offset = self._settings.screen_height // 2 - self._settings.pond_height * self._cell_size // 2

    def _zoom(self, change: int) -> None:
        old = self._cell_size
        self._cell_size = min(max(10, self._cell_size + change), 100)

        if self._cell_size == old:
            return

        # try to zoom at point in the middle
        coor = self.get_visible_grid_coordinates()
        middle = (coor[1] + coor[0]) / 2
        left_half = (max(middle, 0) - max(coor[0], 0)) / 2
        middle = (coor[3] + coor[2]) / 2
        top_half = (max(middle, 0) - max(coor[2], 0)) / 2
        print(left_half, top_half)
        self._x_offset = int(self._x_offset - left_half * change)
        self._y_offset = int(self._y_offset - top_half * change)

    def handle_events(self, events: list[Event]) -> None:
        for event in events:
            if event.event_type == EventType.KEY_PRESSED:
                match event.args["key"]:
                    case "up":
                        self._y_offset -= 50
                    case "down":
                        self._y_offset += 50
                    case "left":
                        self._x_offset -= 50
                    case "right":
                        self._x_offset += 50
                    case "equals":
                        self._zoom(5)
                    case "minus":
                        self._zoom(-5)
