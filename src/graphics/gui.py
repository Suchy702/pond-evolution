import pygame
from pygame.surface import Surface

from src.constants import BLACK, LIGHT_BLUE, GRAY
from src.events.event import GraphicEvent
from src.events.event_emitter import EventEmitter
from src.graphics.graphic_calculator import GraphicCalculator
from src.graphics.graphic_values_guard import GraphicValuesGuard
from src.graphics.image_handler.image_loader import ImageLoader
from src.simulation_settings import SimulationSettings


class GUI:
    def __init__(self, settings: SimulationSettings):
        self.settings: SimulationSettings = settings
        self.vals = GraphicValuesGuard(settings)
        self.calculator = GraphicCalculator(settings)
        self._screen: Surface = pygame.display.set_mode([self.settings.screen_width, self.settings.screen_height])
        self.center_view()
        self._event_emitter = EventEmitter()
        self._image_loader = ImageLoader()

    def draw_empty_frame(self) -> None:
        self._screen.fill(BLACK)
        self.draw_pond_area()

    def draw_pond_area(self) -> None:
        rect_width = self.settings.pond_width * self.vals.cell_size
        rect_height = self.settings.pond_height * self.vals.cell_size
        rect = pygame.Rect(self.vals.x_offset, self.vals.y_offset, rect_width, rect_height)
        pygame.draw.rect(self._screen, LIGHT_BLUE, rect, 0)

    def draw_ui(self) -> None:
        ui_height = self.settings.screen_height - self.settings.screen_pond_height
        rect = pygame.Rect(0, self.settings.screen_pond_height, self.settings.screen_width, ui_height)
        pygame.draw.rect(self._screen, GRAY, rect, 0)

    def _is_visible_now(self, x, y) -> bool:
        x_in = 0 - self.vals.cell_size <= x <= self.settings.screen_pond_width + self.vals.cell_size
        y_in = 0 - self.vals.cell_size <= y <= self.settings.screen_pond_height + self.vals.cell_size
        return x_in and y_in

    def draw_anim_event(self, event: GraphicEvent) -> None:
        x, y = self.calculator.find_pos_to_draw(event, self.vals)
        if self._is_visible_now(x, y):
            self.draw_object(event.pond_object, x, y)

    def center_view(self) -> None:
        self.vals.x_offset, self.vals.y_offset = self.calculator.calc_center_view(self.vals)

    def zoom(self, change: int) -> None:
        self.calculator.calc_zoom(change, self.vals)

    def is_animation_finished(self) -> bool:
        return not self._event_emitter.is_animation_event_present()

    def draw_object(self, obj, x, y) -> None:
        rect = pygame.Rect(x, y, self.vals.cell_size, self.vals.cell_size)
        image = self._image_loader.get_object_image(obj, self.vals.cell_size)
        self._screen.blit(image, rect)
