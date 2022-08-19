import os

import pygame
from pygame import Rect
from pygame.font import Font
from pygame.surface import Surface

import src.constants as const
from src.constants import (
    NUM_OF_SQUARES_IN_PANEL,
    EMPTY_SQUARES,
    BLACK,
    GRAY,
    EDGE_UI_HEIGHT_RATIO,
    TEXT_SIZE_SQUARE_DIM_RATIO,
    TEXT_CENTER_CORRECT_SQUARE_DIM_RATIO,
    X_TEXT_CENTER_SQUARE_DIM_RATIO,
    Y_TEXT_CENTER_SQUARE_DIM_RATIO,
)
from src.graphics.graphic_values_guard import GraphicValuesGuard
from src.graphics.image_handler.image_loader import ImageLoader
from src.logic.engine import Engine
from src.object.dummy_type import DummyType
from src.object.pond_object import PondObject
from src.simulation_settings import SimulationSettings

pygame.font.init()
FONT_PATH = os.path.join('resources', 'font', 'Ubuntu-M.ttf')


class UserPanel:
    def __init__(self, settings: SimulationSettings, screen: Surface, vals: GraphicValuesGuard):
        self._settings: SimulationSettings = settings
        self._vals: GraphicValuesGuard = vals
        self._screen: Surface = screen

        self.image_loader: ImageLoader = None
        self.engine: Engine = None

        # Calculations for panel squares
        self._ui_height: int = self._settings.screen_height - self._settings.screen_pond_height
        self._num_of_squares: int = NUM_OF_SQUARES_IN_PANEL
        self._edge: int = int(self._ui_height*EDGE_UI_HEIGHT_RATIO)
        self._square_dim: int = self._ui_height - self._edge * 2
        self._break: int = self._calc_break()
        self._square_up: int = self._settings.screen_pond_height + self._edge

        self._adding_object_list: list[DummyType] = list(DummyType)
        self._adding_object_idx: int = 0

        self._font: Font = pygame.font.Font(FONT_PATH, int(self._square_dim * TEXT_SIZE_SQUARE_DIM_RATIO))

    @property
    def square_dim(self) -> int:
        return self._square_dim

    def draw(self) -> None:
        self._draw_empty_panel()

        stop = self._num_of_squares*(self._break + self._square_dim)
        for square_idx, x in zip(range(self._num_of_squares), range(self._edge, stop, self._break + self._square_dim)):
            self._choose_what_to_draw(square_idx, x)

    def next_object(self) -> None:
        self._adding_object_idx = (self._adding_object_idx + 1) % len(self._adding_object_list)

    def get_dummy(self) -> PondObject:
        return self.engine.get_dummy(self._adding_object_list[self._adding_object_idx])

    def _get_dummy_img(self) -> Surface:
        return self.image_loader.get_object_image(self.get_dummy(), self._square_dim)

    def _calc_break(self) -> int:
        all_squares_width = self._num_of_squares * self._square_dim
        break_ = (self._settings.screen_width - all_squares_width - self._edge * 2) // (self._num_of_squares - 1)
        if break_ < 0:
            raise Exception("Bad dimensions of panel!")
        return break_

    def _choose_what_to_draw(self, square_idx: int, x: int) -> None:
        match square_idx:
            case const.CURRENT_OBJ_IDX:
                self._draw_current_obj(x)
            case const.CYCLE_COUNT_IDX:
                self._draw_cycle_square(x)
            case _:
                if square_idx not in EMPTY_SQUARES:
                    self._draw_square(x, f"panel_{square_idx}")

    def _draw_current_obj(self, x: int) -> None:
        self._screen.blit(self._get_dummy_img(), self._get_rect(x))

    def _draw_empty_panel(self) -> None:
        rect = pygame.Rect(0, self._settings.screen_pond_height, self._settings.screen_width, self._ui_height)
        pygame.draw.rect(self._screen, GRAY, rect, 0)

    def _draw_square(self, x: int, name: str) -> None:
        self._screen.blit(self.image_loader.get_ui_image(name), self._get_rect(x))

    def _get_rect(self, x: int) -> Rect:
        return pygame.Rect(x, self._square_up, self._square_dim, self._square_dim)

    def _calc_text_rendering_pos(self, x: int) -> tuple[int, int]:
        correct = (len(str(self.engine.cycle_count)) - 1) * self._square_dim * TEXT_CENTER_CORRECT_SQUARE_DIM_RATIO
        x_pos = x + int(self._square_dim * X_TEXT_CENTER_SQUARE_DIM_RATIO - correct)
        y_pos = self._settings.screen_pond_height + int(self._ui_height*Y_TEXT_CENTER_SQUARE_DIM_RATIO)
        return x_pos, y_pos

    def _render_cycles_count_text(self, x: int) -> None:
        text_surface = self._font.render(str(self.engine.cycle_count), True, BLACK)
        self._screen.blit(text_surface, self._calc_text_rendering_pos(x))

    def _draw_cycle_square(self, x: int) -> None:
        self._draw_square(x, "panel_11")
        self._render_cycles_count_text(x)
