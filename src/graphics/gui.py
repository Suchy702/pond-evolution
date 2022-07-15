import pygame
from pygame.surface import Surface

from src.constants import BLACK, LIGHT_BLUE, GRAY
from src.events.event_emitter import EventEmitter
from src.graphics.image_handler.utility import get_object_image
from src.simulation_settings import SimulationSettings
from src.graphics.graphic_values_guard import GraphicValuesGuard
from src.graphics.graphic_calculator import GraphicCalculator
from src.events.event import GraphicEvent


class GUI:
    def __init__(self, settings: SimulationSettings):
        self.settings: SimulationSettings = settings
        self.vals = GraphicValuesGuard(settings)
        self.calculator = GraphicCalculator(settings)
        self._screen: Surface = pygame.display.set_mode([self.settings.screen_width, self.settings.screen_height])
        self.center_view()
        self._event_emitter = EventEmitter()

    def draw_empty_frame(self) -> None:
        self._screen.fill(BLACK)
        self.draw_pond_area()

    def draw_pond_area(self):
        rect_width = self.settings.pond_width * self.vals.cell_size
        rect_height = self.settings.pond_height * self.vals.cell_size
        rect = pygame.Rect(self.vals.x_offset, self.vals.y_offset, rect_width, rect_height)
        pygame.draw.rect(self._screen, LIGHT_BLUE, rect, 0)

    def draw_ui(self):
        ui_height = self.settings.screen_height - self.settings.screen_pond_height
        rect = pygame.Rect(0, self.settings.screen_pond_height, self.settings.screen_width, ui_height)
        pygame.draw.rect(self._screen, GRAY, rect, 0)

    def _is_visible_now(self, x: int, y: int):
        x_in = 0 <= x <= self.settings.screen_pond_width
        y_in = 0 <= y <= self.settings.screen_pond_height
        return x_in and y_in

    def draw_anim_event(self, event: GraphicEvent):
        x, y = self.calculator.find_pos_to_draw(event, self.vals)
        if self._is_visible_now(x, y):
            self.draw_object(event.pond_object, x, y)

    def center_view(self) -> None:
        self.vals.x_offset, self.vals.y_offset = self.calculator.calc_center_view(self.vals)

    def zoom(self, change: int) -> None:
        self.calculator.change_vals_to_zoom(change, self.vals)

    def is_animation_finished(self):
        return not self._event_emitter.is_animation_event_present()

    def draw_object(self, obj, x, y):
        rect = pygame.Rect(x, y, self.vals.cell_size, self.vals.cell_size)
        image = get_object_image(obj)
        self._screen.blit(pygame.transform.scale(image, (self.vals.cell_size, self.vals.cell_size)), rect)
