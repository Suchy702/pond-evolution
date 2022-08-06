from typing import cast

import pygame
from pygame.surface import Surface

from src.constants import LIGHT_BLUE, FISH_MAX_SIZE, FISH_MIN_SIZE, CELL_MIN_PX_SIZE, CELL_MAX_PX_SIZE
from src.events.event import GraphicEvent
from src.events.event_emitter import EventEmitter
from src.graphics.graphic_calculator import GraphicCalculator
from src.graphics.graphic_values_guard import GraphicValuesGuard, clip
from src.graphics.image_handler.image_loader import ImageLoader
from src.graphics.ui import UI
from src.object.fish import Fish
from src.object.object_kind import ObjectKind
from src.simulation_settings import SimulationSettings


class GUI:
    def __init__(self, settings: SimulationSettings, engine):
        self.settings: SimulationSettings = settings
        self.vals = GraphicValuesGuard(settings)
        self.calculator = GraphicCalculator(settings)

        screen_flags = pygame.SCALED | pygame.FULLSCREEN if self.settings.fullscreen else 0
        self._screen: Surface = pygame.display.set_mode(
            [self.settings.screen_width, self.settings.screen_height], flags=screen_flags, vsync=1
        )
        self.center_view()

        self._event_emitter = EventEmitter()

        self.ui = UI(self.settings, self._screen, self.vals)

        self._image_loader = ImageLoader(self.ui.square_dim)

        self.ui.set_image_loader(self._image_loader)
        self.ui.set_engine(engine)

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
        x, y = self.calculator.find_pos_to_draw(event, self.vals)
        if self._is_visible_now(x, y):
            self.draw_object(event, x, y)

    def center_view(self) -> None:
        self.vals.x_offset, self.vals.y_offset = self.calculator.calc_center_view(self.vals)

    def zoom(self, change: int) -> None:
        self.calculator.calc_zoom(change, self.vals)

    def is_animation_finished(self) -> bool:
        return not self._event_emitter.is_animation_event_present()

    def draw_object(self, event: GraphicEvent, x: int, y: int) -> None:
        size = self.vals.cell_size
        if event.pond_object.kind == ObjectKind.FISH:
            fish = cast(Fish, event.pond_object)
            size = int(fish.size / ((FISH_MAX_SIZE + FISH_MIN_SIZE) // 2) * self.vals.cell_size)
            size = clip(size, CELL_MIN_PX_SIZE, CELL_MAX_PX_SIZE)
        image = self._image_loader.get_object_image(event.pond_object, size)

        if event.is_flipped:
            image = pygame.transform.flip(image, True, False)
        if event.rotate is not None:
            image = pygame.transform.rotate(image, event.rotate)

        x += (self.vals.cell_size - size) // 2
        y += (self.vals.cell_size - size) // 2

        self._screen.blit(image, (x, y))

    def get_click_coor(self, click_pos: tuple[int, int]) -> tuple[int, int]:
        return self.calculator.get_click_coor(click_pos, self.vals)
