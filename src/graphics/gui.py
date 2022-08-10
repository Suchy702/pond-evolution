import pygame
from pygame.surface import Surface

from src.constants import LIGHT_BLUE
from src.events.event import GraphicEvent
from src.events.event_emitter import EventEmitter
from src.graphics.graphic_calculator import GraphicCalculator
from src.graphics.graphic_values_guard import GraphicValuesGuard
from src.graphics.image_handler.image_loader import ImageLoader
from src.graphics.user_panel import UserPanel
from src.logic.engine import Engine
from src.object.object_kind import ObjectKind
from src.simulation_settings import SimulationSettings


class GUI:
    def __init__(self, settings: SimulationSettings, engine: Engine):
        self.settings: SimulationSettings = settings
        self.vals: GraphicValuesGuard = GraphicValuesGuard(settings)
        self.calcus: GraphicCalculator = GraphicCalculator(settings)

        screen_flags = pygame.SCALED | pygame.FULLSCREEN if self.settings.fullscreen else 0
        screen_resolution = [self.settings.screen_width, self.settings.screen_height]
        self._screen: Surface = pygame.display.set_mode(screen_resolution, flags=screen_flags, vsync=1)
        self.center_view()

        self._event_emitter = EventEmitter()

        self.user_panel = UserPanel(self.settings, self._screen, self.vals)

        self._image_loader = ImageLoader(self.user_panel.square_dim)

        self.user_panel.set_image_loader(self._image_loader)
        self.user_panel.set_engine(engine)

    def draw_empty_frame(self) -> None:
        self.draw_pond_area()

    def draw_pond_area(self) -> None:
        rect_width = self.settings.pond_width * self.vals.cell_size
        rect_height = self.settings.pond_height * self.vals.cell_size
        rect = pygame.Rect(self.vals.x_offset, self.vals.y_offset, rect_width, rect_height)
        pygame.draw.rect(self._screen, LIGHT_BLUE, rect, 0)

    def _is_visible_now(self, x, y) -> bool:
        x_in: bool = 0 - self.vals.cell_size <= x <= self.settings.screen_pond_width + self.vals.cell_size
        y_in: bool = 0 - self.vals.cell_size <= y <= self.settings.screen_pond_height + self.vals.cell_size
        return x_in and y_in

    def draw_anim_event(self, event: GraphicEvent) -> None:
        x, y = self.calcus.find_pos_to_draw(event, self.vals)
        if self._is_visible_now(x, y):
            self.draw_object(event, x, y)

    def center_view(self) -> None:
        self.vals.x_offset, self.vals.y_offset = self.calcus.calc_center_view(self.vals)

    def zoom(self, change: int) -> None:
        self.calcus.calc_zoom(change, self.vals)

    def is_animation_finished(self) -> bool:
        return not self._event_emitter.is_animation_event_present()

    @staticmethod
    def is_obj_fish(event: GraphicEvent) -> bool:
        return event.pond_object.kind == ObjectKind.FISH

    def _get_reformed_image(self, event: GraphicEvent, size: int) -> Surface:
        image = self._image_loader.get_object_image(event.pond_object, size)
        if event.is_flipped:
            image = pygame.transform.flip(image, True, False)
        if event.rotate is not None:
            image = pygame.transform.rotate(image, event.rotate)
        return image

    def draw_object(self, event: GraphicEvent, x: int, y: int) -> None:
        size = self.calcus.match_size_for_fish(event, self.vals) if self.is_obj_fish(event) else self.vals.cell_size
        image = self._get_reformed_image(event, size)
        x, y = self.calcus.reform_pos_to_be_in_center(x, y, self.vals, size)
        self._screen.blit(image, (x, y))

    def get_click_coor(self, click_pos: tuple[int, int]) -> tuple[int, int]:
        return self.calcus.get_click_coor(click_pos, self.vals)

    def hide_screen(self) -> None:
        self._screen = pygame.display.set_mode((0, 0), pygame.HIDDEN)
