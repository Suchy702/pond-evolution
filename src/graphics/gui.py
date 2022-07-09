from math import ceil

import pygame
from pygame.surface import Surface

from src.events.event import Event, EventType
from src.events.event_handler import EventHandler
from src.events.event_manager import EventManager
from src.graphics.image_handler.utility import get_object_image
from src.object_handler.pond_object_handler import PondObjectHandler
from src.simulation_settings import SimulationSettings

VERBOSE = True


class GUI(EventHandler):
    def __init__(self, settings: SimulationSettings, handlers: list[PondObjectHandler]):
        self._settings: SimulationSettings = settings

        self._screen: Surface = pygame.display.set_mode([self._settings.screen_width, self._settings.screen_height])
        self._cell_size: int = 20  # length of square cell in px
        self._x_offset: int = 0
        self._y_offset: int = 0
        self._center_view()

        self._event_handler = EventManager()

    def draw_frame(self) -> None:
        self._screen.fill((0, 0, 0))
        self.draw_boundary()
        pygame.display.update()

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

    def clip_x(self, min_x, max_x) -> tuple[int, int]:
        return max(min_x, 0), min(max_x, self._settings.pond_width - 1)

    def clip_y(self, min_y, max_y) -> tuple[int, int]:
        return max(min_y, 0), min(max_y, self._settings.pond_height - 1)

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
        self._x_offset = int(self._x_offset - left_half * change)
        self._y_offset = int(self._y_offset - top_half * change)

    def is_animation_finished(self):
        return not self._event_handler.is_animation_event()

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
                    case "=":
                        self._zoom(5)
                    case "-":
                        self._zoom(-5)
                    case "c":
                        self._center_view()

    def handle_animation_events(self, events: list[Event]) -> None:
        for event in events:
            self._handle_animation_event(event)
        pygame.display.update()

    def draw_object(self, obj, x, y):
        # TODO: teraz mozemy rysowac obrazki o dowolnym ration, wiec mozna zmienic self._cell_size na co innego
        rect = pygame.Rect(x, y, self._cell_size, self._cell_size)

        image = get_object_image(obj)
        self._screen.blit(pygame.transform.scale(image, (self._cell_size, self._cell_size)), rect)

    def _handle_animation_event(self, event: Event):
        x, y = None, None

        if event.event_type == EventType.ANIM_MOVE:
            if 'total_steps' not in event.args:
                event.args['step'] = 1
                event.args['total_steps'] = self._settings.animation_speed

            x1 = event.args['from_x'] * self._cell_size + self._x_offset
            y1 = event.args['from_y'] * self._cell_size + self._y_offset
            x2 = event.args['to_x'] * self._cell_size + self._x_offset
            y2 = event.args['to_y'] * self._cell_size + self._y_offset
            dist = y2 - y1

            if x1 == x2:
                y = y1 + dist * event.args['step'] / event.args['total_steps']
                x = x1
            else:
                a = (y2 - y1) / (x2 - x1)
                b = y1 - a * x1

                x = x1 + dist * event.args['step'] / event.args['total_steps']
                y = a * x + b

                if event.args['step'] < event.args['total_steps']:
                    n_event = event.copy()
                    n_event.args['step'] += 1
                    self._event_handler.emit_event(n_event)

        elif event.event_type == EventType.ANIM_STAY:
            x = event.args['x'] * self._cell_size + self._x_offset
            y = event.args['y'] * self._cell_size + self._y_offset

            n_event = event.copy()
            self._event_handler.emit_event(n_event)

        self.draw_object(event.args['object'], x, y)
