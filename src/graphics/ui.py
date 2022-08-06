import pygame

from src.constants import GRAY, FISH_MIN_SIZE, FISH_MAX_SIZE
from src.graphics.graphic_values_guard import GraphicValuesGuard
from src.graphics.image_handler.image_loader import ImageLoader
from src.object.alga import Alga
from src.object.alga_maker import AlgaMaker
from src.object.fish import Fish
from src.object.fish_trait import FishTrait
from src.object.fish_type import FishType
from src.object.worm import Worm
from src.position import Position
from src.simulation_settings import SimulationSettings

pygame.font.init()
FONT = pygame.font.SysFont(pygame.font.get_default_font(), 30)


class UI:
    def __init__(self, settings: SimulationSettings, screen, vals: GraphicValuesGuard):
        self.settings = settings
        self._vals = vals
        self._screen = screen
        self._image_loader = None
        self._adding_object = Fish(10, 10, 3, Position(-1, -1))

        self.ui_height = self.settings.screen_height - self.settings.screen_pond_height
        self.num_of_squares = 12
        self.edge = int(self.ui_height * 0.03)
        self.square_dim = self.ui_height - self.edge*2
        self.break_ = self.calc_break()

        self.square_up = self.settings.screen_pond_height + self.edge

        self._adding_object_list = ["fish_herbi", "fish_carni", "fish_omni", "fish_predator",
                                    "worm", "alga", "alga_maker"]
        self._adding_object_dummies = []
        self._initialize_adding_dummies()
        self._adding_object_idx = 0

    @property
    def adding_object(self):
        return self._adding_object_list[self._adding_object_idx], self._adding_object_dummies[self._adding_object_idx]

    def set_image_loader(self, img_loader):
        self._image_loader = img_loader

    def calc_break(self):
        all_squares_width = self.num_of_squares*self.square_dim
        break_ = (self.settings.screen_width - all_squares_width - self.edge*2) // (self.num_of_squares-1)
        if break_ < 0:
            raise Exception("Bad dimensions of panel!")
        return break_

    def next_add_object(self):
        self._adding_object_idx = (self._adding_object_idx + 1) % len(self._adding_object_list)

    def _add_fishes_dummies(self):
        size = (FISH_MIN_SIZE + FISH_MAX_SIZE) // 2
        for fish_type in [FishType.HERBIVORE, FishType.CARNIVORE, FishType.OMNIVORE, FishType.CARNIVORE]:
            fish = Fish(-1, size, -1, Position(-1, -1))
            fish.fish_type = fish_type
            self._adding_object_dummies.append(fish)
        self._adding_object_dummies[-1].traits.add(FishTrait.PREDATOR)

    @staticmethod
    def _get_other_dummies():
        other_dummies = [
            Worm(-1, Position(-1, -1), (-1, -1)),
            Alga(-1, Position(-1, -1), -1),
            AlgaMaker(Position(-1, -1), -1),
        ]
        return other_dummies

    def _initialize_adding_dummies(self):
        self._add_fishes_dummies()
        self._adding_object_dummies.extend(self._get_other_dummies())

    def _get_dummy_img(self):
        add_obj_dummy = self._adding_object_dummies[self._adding_object_idx]
        return self._image_loader.get_object_image(add_obj_dummy, self.square_dim)

    def _get_rect(self, x):
        return pygame.Rect(x, self.square_up, self.square_dim, self.square_dim)

    def _draw_act_adding_obj(self, x):
        self._screen.blit(self._get_dummy_img(), self._get_rect(x))

    def _draw_empty_panel(self):
        rect = pygame.Rect(0, self.settings.screen_pond_height, self.settings.screen_width, self.ui_height)
        pygame.draw.rect(self._screen, GRAY, rect, 0)

    def _draw_square(self, x, name):
        self._screen.blit(self._image_loader.get_ui_image(name), self._get_rect(x))

    def _draw_cycle_square(self, x):
        self._draw_square(x, "panel_11")

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
