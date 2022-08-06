import pygame

from src.constants import GRAY
from src.graphics.graphic_values_guard import GraphicValuesGuard
from src.object.dummy_type import DummyType
from src.simulation_settings import SimulationSettings

pygame.font.init()
FONT = pygame.font.SysFont("Comic Sans MS", 30)


class UI:
    def __init__(self, settings: SimulationSettings, screen, vals: GraphicValuesGuard):
        self.settings = settings
        self._vals = vals
        self._screen = screen
        self._image_loader = None
        self._engine = None

        self.ui_height = self.settings.screen_height - self.settings.screen_pond_height
        self.num_of_squares = 12
        self.edge = int(self.ui_height * 0.08)
        self.square_dim = self.ui_height - self.edge * 2
        self.break_ = self.calc_break()

        self.square_up = self.settings.screen_pond_height + self.edge

        self._adding_object_list = list(DummyType)
        self._adding_object_idx = 0

    def set_engine(self, engine):
        self._engine = engine

    def set_image_loader(self, img_loader):
        self._image_loader = img_loader

    def calc_break(self):
        all_squares_width = self.num_of_squares * self.square_dim
        break_ = (self.settings.screen_width - all_squares_width - self.edge * 2) // (self.num_of_squares - 1)
        if break_ < 0:
            raise Exception("Bad dimensions of panel!")
        return break_

    def next_add_object(self):
        self._adding_object_idx = (self._adding_object_idx + 1) % len(self._adding_object_list)

    def get_dummy(self):
        return self._engine.get_dummy(self._adding_object_list[self._adding_object_idx])

    def _get_dummy_img(self):
        return self._image_loader.get_object_image(self.get_dummy(), self.square_dim)

    def _get_rect(self, x):
        return pygame.Rect(x, self.square_up, self.square_dim, self.square_dim)

    def _draw_act_adding_obj(self, x):
        self._screen.blit(self._get_dummy_img(), self._get_rect(x))

    def _draw_empty_panel(self):
        rect = pygame.Rect(0, self.settings.screen_pond_height, self.settings.screen_width, self.ui_height)
        pygame.draw.rect(self._screen, GRAY, rect, 0)

    def _draw_square(self, x, name):
        self._screen.blit(self._image_loader.get_ui_image(name), self._get_rect(x))

    def _calc_text_rendering_pos(self, x):
        try_center = (len(str(self._engine.cycle_count)) - 1)*self.square_dim*0.08
        x_pos = x + int(self.square_dim * 0.4) - try_center
        y_pos = self.settings.screen_pond_height + int(self.ui_height * 0.5)
        return x_pos, y_pos

    def _render_cycles_count_text(self, x):
        text_surface = FONT.render(str(self._engine.cycle_count), False, (0, 0, 0))
        self._screen.blit(text_surface, self._calc_text_rendering_pos(x))

    def _draw_cycle_square(self, x):
        self._draw_square(x, "panel_11")
        self._render_cycles_count_text(x)

    def _draw_stats_square(self, x):
        pass

    def draw(self) -> None:
        self._draw_empty_panel()
        empty_squares = {2, 6, 9}

        x = self.edge
        for i in range(self.num_of_squares):
            match i:
                case 1:
                    self._draw_act_adding_obj(x)
                case 11:
                    self._draw_cycle_square(x)
                case _:
                    if i not in empty_squares:
                        self._draw_square(x, f"panel_{i}")
            x += self.break_ + self.square_dim
