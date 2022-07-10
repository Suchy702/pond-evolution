from math import ceil

import pygame
from pygame.surface import Surface

from src.events.event import Event, EventType
from src.events.event_handler import EventHandler
from src.events.event_manager import EventManager
from src.graphics.image_handler.utility import get_object_image
from src.simulation_settings import SimulationSettings
from src.constants import CELL_MIN_PX_SIZE, CELL_MAX_PX_SIZE, MOVE_SCREEN_BY_CLICK, ZOOM_SCREEN_BY_CLICK

VERBOSE = True


class GUI(EventHandler):
    def __init__(self, settings: SimulationSettings):
        self._settings: SimulationSettings = settings

        self._screen: Surface = pygame.display.set_mode([self._settings.screen_width, self._settings.screen_height])
        #self._screen: Surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self._cell_size: int = CELL_MIN_PX_SIZE  # length of square cell in px
        self._x_offset: int = 0
        self._y_offset: int = 0
        self._center_view()

        self._event_handler = EventManager()

    def draw_empty_frame(self) -> None:
        self._screen.fill((0, 0, 0))
        self.draw_boundary()

    # Get indices of cells that are fully visible
    def get_visible_grid_coordinates(self) -> tuple[int, int, int, int]:
        x_min = int(ceil(-self._x_offset / self._cell_size))
        x_max = (self._settings.screen_width - self._cell_size - self._x_offset) // self._cell_size

        y_min = int(ceil(-self._y_offset / self._cell_size))
        y_max = (self._settings.screen_height - self._cell_size - self._y_offset) // self._cell_size

        return x_min, x_max, y_min, y_max

    def draw_boundary(self):
        rect = pygame.Rect(
            self._x_offset, self._y_offset,
            self._settings.pond_width * self._cell_size, self._settings.pond_height * self._cell_size
        )
        pygame.draw.rect(self._screen, (255, 255, 255), rect, 0)

    def _center_view(self) -> None:
        self._x_offset = self._settings.screen_width // 2 - self._settings.pond_width * self._cell_size // 2
        self._y_offset = self._settings.screen_height // 2 - self._settings.pond_height * self._cell_size // 2

    @staticmethod
    def _calc_left_half(x1, x2) -> float:
        middle = (x1 + x2) / 2
        return (middle - x1) / 2

    @staticmethod
    def _calc_top_half(y1, y2) -> float:
        middle = (y1 + y2) / 2
        return (middle - y1) / 2

    def _zoom(self, change: int) -> None:
        old = self._cell_size
        self._cell_size = min(max(CELL_MIN_PX_SIZE, self._cell_size + change), CELL_MAX_PX_SIZE)

        if self._cell_size == old:
            return

        # try to zoom at point in the middle
        coor = self.get_visible_grid_coordinates()
        self._change_x_offset(int(-self._calc_left_half(coor[0], coor[1]) * change))
        self._change_y_offset(int(-self._calc_top_half(coor[2], coor[3]) * change))

    def is_animation_finished(self):
        return not self._event_handler.is_animation_event()

    def _change_y_offset(self, val) -> None:
        y_offset_limit = -(self._settings.pond_height * self._cell_size - self._settings.screen_height)
        self._y_offset = max(min(self._y_offset + val, 0), y_offset_limit)

    def _change_x_offset(self, val) -> None:
        x_offset_limit = -(self._settings.pond_width * self._cell_size - self._settings.screen_width)
        self._x_offset = max(min(self._x_offset + val, 0), x_offset_limit)

    def handle_events(self, events: list[Event]) -> None:
        for event in events:
            if event.type == EventType.KEY_PRESSED:
                match event.args["key"]:
                    case "down":
                        self._change_y_offset(-MOVE_SCREEN_BY_CLICK)
                    case "up":
                        self._change_y_offset(MOVE_SCREEN_BY_CLICK)
                    case "right":
                        self._change_x_offset(-MOVE_SCREEN_BY_CLICK)
                    case "left":
                        self._change_x_offset(MOVE_SCREEN_BY_CLICK)
                    case "=":
                        self._zoom(ZOOM_SCREEN_BY_CLICK)
                    case "-":
                        self._zoom(-ZOOM_SCREEN_BY_CLICK)
                    case "c":
                        self._center_view()
                    case ",":
                        self._settings.animation_speed = min(100, self._settings.animation_speed + 1)
                    case ".":
                        self._settings.animation_speed = max(1, self._settings.animation_speed - 1)

    def handle_animation_events(self, events: list[Event]) -> None:
        self.draw_empty_frame()
        for event in events:
            self._handle_animation_event(event)
        pygame.display.update()

    def draw_object(self, obj, x, y):
        rect = pygame.Rect(x, y, self._cell_size, self._cell_size)

        image = get_object_image(obj)
        self._screen.blit(pygame.transform.scale(image, (self._cell_size, self._cell_size)), rect)

    def _handle_animation_event(self, event: Event):
        if 'total_steps' not in event.args:
            event.args['step'] = 1
            event.args['total_steps'] = self._settings.animation_speed

        x, y = None, None

        if event.type == EventType.ANIM_MOVE:
            x1 = event.args['from_x'] * self._cell_size + self._x_offset
            y1 = event.args['from_y'] * self._cell_size + self._y_offset
            x2 = event.args['to_x'] * self._cell_size + self._x_offset
            y2 = event.args['to_y'] * self._cell_size + self._y_offset

            if x1 == x2:
                dist = y2 - y1
                y = y1 + dist * event.args['step'] / event.args['total_steps']
                x = x1
            else:
                dist = x2 - x1
                a = (y2 - y1) / (x2 - x1)
                b = y1 - a * x1

                x = x1 + dist * event.args['step'] / event.args['total_steps']
                y = a * x + b

        elif event.type == EventType.ANIM_STAY:
            x = event.args['x'] * self._cell_size + self._x_offset
            y = event.args['y'] * self._cell_size + self._y_offset

        if event.args['step'] < event.args['total_steps']:
            n_event = event.copy()
            n_event.args['step'] += 1
            self._event_handler.emit_event(n_event)

        self.draw_object(event.args['object'], x, y)
