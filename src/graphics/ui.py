import pygame

from src.constants import GRAY
from src.graphics.graphic_values_guard import GraphicValuesGuard
from src.graphics.image_handler.image_loader import ImageLoader
from src.object.alga import Alga
from src.object.alga_maker import AlgaMaker
from src.object.fish import Fish
from src.object.fish_type import FishType
from src.object.worm import Worm
from src.position import Position
from src.simulation_settings import SimulationSettings

pygame.font.init()
FONT = pygame.font.SysFont(pygame.font.get_default_font(), 30)


class UI:
    def __init__(self, settings: SimulationSettings, screen, image_loader: ImageLoader, vals: GraphicValuesGuard):
        self.settings = settings
        self._vals = vals
        self._screen = screen
        self._image_loader = image_loader
        self._adding_object = Fish(10, 10, 3, Position(-1, -1))
        self.ui_height = self.settings.screen_height - self.settings.screen_pond_height

        self._adding_object_list = ["fish_herbi", "fish_carni", "fish_omni", "worm", "alga", "alga_maker"]
        self._adding_object_dummies = self._initialize_adding_dummies()
        self._adding_object_idx = 0

    @property
    def adding_object(self):
        return self._adding_object_list[self._adding_object_idx], self._adding_object_dummies[self._adding_object_idx]

    def next_add_object(self):
        self._adding_object_idx = (self._adding_object_idx + 1) % len(self._adding_object_list)

    def _initialize_adding_dummies(self):
        fish_herbi = Fish(-1, -1, -1, Position(-1, -1))
        fish_herbi.fish_type = FishType.HERBIVORE

        fish_carni = Fish(-1, -1, -1, Position(-1, -1))
        fish_carni.fish_type = FishType.CARNIVORE

        fish_omni = Fish(-1, -1, -1, Position(-1, -1))
        fish_omni.fish_type = FishType.OMNIVORE

        adding_object_dummies = [
            fish_herbi,
            fish_carni,
            fish_omni,
            Worm(-1, Position(-1, -1), (-1, -1)),
            Alga(-1, Position(-1, -1), -1),
            AlgaMaker(Position(-1, -1), -1),
        ]

        return adding_object_dummies

    def _draw_act_adding_obj(self):
        add_obj_dummy = self._adding_object_dummies[self._adding_object_idx]
        img = self._image_loader.get_object_image(add_obj_dummy, 80)
        self._screen.blit(img, pygame.Rect(0, self.settings.screen_height - self.ui_height, 80, 80))

    def draw(self) -> None:
        rect = pygame.Rect(0, self.settings.screen_pond_height, self.settings.screen_width, self.ui_height)
        pygame.draw.rect(self._screen, GRAY, rect, 0)
        self._draw_act_adding_obj()
