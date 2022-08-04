import pygame

from src.constants import GRAY

from src.object.fish import Fish
from src.position import Position

pygame.font.init()
FONT = pygame.font.SysFont(pygame.font.get_default_font(), 30)


class UI:
    def __init__(self, settings, screen, image_loader):
        self.settings = settings
        self._screen = screen
        self._image_loader = image_loader
        self._adding_object = Fish(10, 10, 3, Position(-1, -1))

    @property
    def adding_object(self):
        return Fish(10, 10, 3, Position(-1, -1))

    def draw(self) -> None:
        ui_height = self.settings.screen_height - self.settings.screen_pond_height
        rect = pygame.Rect(0, self.settings.screen_pond_height, self.settings.screen_width, ui_height)
        pygame.draw.rect(self._screen, GRAY, rect, 0)

        ui_components = [
            'plus', 'arrow3', 'omnivore_fish', 'arrow3', 'spacer', 'arrow3', 'spacer', 'magnifying_glass', 'spacer',
            'cycle', 'spacer'
        ]

        for idx, ui_component in enumerate(ui_components):
            self._draw_ui_component(ui_component, idx, len(ui_components))

    def _draw_ui_component(self, name: str, idx: int, total: int) -> None:
        img = None

        if name == 'spacer':
            return
        elif name == 'cycle':
            img = FONT.render('Cycle: ', True, (0, 0, 0))
        else:
            img = self._image_loader.get_ui_image(name)

        cell_width = self.settings.screen_width // total
        ui_height = self.settings.screen_height - self.settings.screen_pond_height
        x_coor = idx * cell_width + (cell_width - img.get_width()) // 2
        y_coor = self.settings.screen_pond_height + (ui_height - img.get_height()) // 2

        rect = pygame.Rect(x_coor, y_coor, img.get_width(), img.get_height())

        self._screen.blit(img, rect)

    def change_adding_object(self):
        pass