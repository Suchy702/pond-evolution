import pygame
import src.constants as const

from src.constants import (
    NUM_OF_SQUARES_IN_PANEL,
    EMPTY_SQUARES,
    BLACK,
    EDGE_UI_HEIGHT_PART,
    TEXT_SIZE_SQUARE_DIM_PART,
    TEXT_CENTER_CORRECT_SQUARE_DIM_PART,
    X_TEXT_CENTER_SQUARE_DIM_PART,
    Y_TEXT_CENTER_SQUARE_DIM_PART,
)

from pygame import Surface
from pygame import Rect
from pygame.font import Font
from pygame.surface import SurfaceType  # type: ignore

from src.constants import GRAY
from src.graphics.graphic_values_guard import GraphicValuesGuard
from src.object.dummy_type import DummyType
from src.object.pond_object import PondObject
from src.simulation_settings import SimulationSettings
from src.graphics.image_handler.image_loader import ImageLoader
from src.logic.engine import Engine

pygame.font.init()


class UI:
    def __init__(self, settings: SimulationSettings, screen: Surface, vals: GraphicValuesGuard):
        self._settings: SimulationSettings = settings
        self._vals: GraphicValuesGuard = vals
        self._screen: Surface = screen

        # TODO: Co z tym zrobic? Wgl czy UI moze miec Engine? wydaje mi sie ze to moze miec tylko game i event_manager
        self._image_loader: ImageLoader = None
        self._engine: Engine = None

        # Calculations for panel squares
        self._ui_height: int = self._settings.screen_height - self._settings.screen_pond_height
        self._num_of_squares: int = NUM_OF_SQUARES_IN_PANEL
        self._edge: int = int(self._ui_height*EDGE_UI_HEIGHT_PART)
        self._square_dim: int = self._ui_height - self._edge * 2
        self._break: int = self._calc_break()
        self._square_up: int = self._settings.screen_pond_height + self._edge

        self._adding_object_list: list[DummyType] = list(DummyType)
        self._adding_object_idx: int = 0

        self._font: Font = pygame.font.SysFont("Comic Sans MS", int(self._square_dim * TEXT_SIZE_SQUARE_DIM_PART))

    @property
    def square_dim(self) -> int:
        return self._square_dim

    def set_engine(self, engine: Engine) -> None:
        self._engine = engine

    def set_image_loader(self, img_loader: ImageLoader) -> None:
        self._image_loader = img_loader

    def _calc_break(self) -> int:
        all_squares_width = self._num_of_squares * self._square_dim
        break_ = (self._settings.screen_width - all_squares_width - self._edge * 2) // (self._num_of_squares - 1)
        if break_ < 0:
            raise Exception("Bad dimensions of panel!")
        return break_

    def next_add_object(self) -> None:
        self._adding_object_idx = (self._adding_object_idx + 1) % len(self._adding_object_list)

    def get_dummy(self) -> PondObject:
        return self._engine.get_dummy(self._adding_object_list[self._adding_object_idx])

    def _get_dummy_img(self) -> Surface | SurfaceType:
        return self._image_loader.get_object_image(self.get_dummy(), self._square_dim)

    def _get_rect(self, x: int) -> Rect:
        return pygame.Rect(x, self._square_up, self._square_dim, self._square_dim)

    def _draw_act_adding_obj(self, x: int) -> None:
        self._screen.blit(self._get_dummy_img(), self._get_rect(x))

    def _draw_empty_panel(self) -> None:
        rect = pygame.Rect(0, self._settings.screen_pond_height, self._settings.screen_width, self._ui_height)
        pygame.draw.rect(self._screen, GRAY, rect, 0)

    def _draw_square(self, x: int, name: str) -> None:
        self._screen.blit(self._image_loader.get_ui_image(name), self._get_rect(x))

    def _calc_text_rendering_pos(self, x: int) -> tuple[int, int]:
        correct = (len(str(self._engine.cycle_count)) - 1) * self._square_dim * TEXT_CENTER_CORRECT_SQUARE_DIM_PART
        x_pos = x + int(self._square_dim * X_TEXT_CENTER_SQUARE_DIM_PART - correct)
        y_pos = self._settings.screen_pond_height + int(self._ui_height*Y_TEXT_CENTER_SQUARE_DIM_PART)
        return x_pos, y_pos

    def _render_cycles_count_text(self, x: int) -> None:
        text_surface = self._font.render(str(self._engine.cycle_count), True, BLACK)
        self._screen.blit(text_surface, self._calc_text_rendering_pos(x))

    def _draw_cycle_square(self, x: int) -> None:
        self._draw_square(x, "panel_11")
        self._render_cycles_count_text(x)

    def _choose_what_to_draw(self, square_idx: int, x: int) -> None:
        match square_idx:
            case const.ADDING_OBJ_IDX:
                self._draw_act_adding_obj(x)
            case const.CYCLE_COUNT_IDX:
                self._draw_cycle_square(x)
            case _:
                if square_idx not in EMPTY_SQUARES:
                    self._draw_square(x, f"panel_{square_idx}")

    def draw(self) -> None:
        self._draw_empty_panel()

        stop = self._num_of_squares*(self._break + self._square_dim)
        for square_idx, x in zip(range(self._num_of_squares), range(self._edge, stop, self._break + self._square_dim)):
            self._choose_what_to_draw(square_idx, x)
