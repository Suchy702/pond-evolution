import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_MINUS,
    K_EQUALS,
    QUIT
)

from src.constants import FPS
from src.engine import Engine
from src.gui import GUI
from src.simulation_settings import SimulationSettings


class Game:
    def __init__(self):
        self._settings = SimulationSettings()
        self._settings.pond_width = 20
        self._settings.pond_height = 20

        self._engine = Engine(self._settings)
        self._gui = GUI(self._settings, [])

    def run(self) -> None:
        clock = pygame.time.Clock()
        running = True

        while running:
            clock.tick(FPS)

            self._gui.draw_frame()
            running = self.handle_events()

    def handle_events(self) -> bool:
        running = True
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[K_UP]:
            self._gui.y_offset -= 50
        elif keys[K_DOWN]:
            self._gui.y_offset += 50
        elif keys[K_LEFT]:
            self._gui.x_offset -= 50
        elif keys[K_RIGHT]:
            self._gui.x_offset += 50
        elif keys[K_EQUALS]:
            self._gui.cell_size += 5
        elif keys[K_MINUS]:
            self._gui.cell_size -= 5

        return running
