import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_MINUS,
    K_EQUALS,
    KEYDOWN,
    QUIT
)

from src.constants import FPS
from src.engine import Engine
from src.gui import GUI
from src.simulation_settings import SimulationSettings


class Game:
    def __init__(self):
        self._settings = SimulationSettings()
        self._settings.pond_width = 10
        self._settings.pond_height = 10

        self._engine = Engine(self._settings)
        self._gui = GUI(self._settings, [])

    def run(self) -> None:
        clock = pygame.time.Clock()
        running = True

        while running:
            clock.tick(FPS)

            self._gui.draw_frame()

            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_UP:
                        self._gui.y_offset -= 50
                    elif event.key == K_DOWN:
                        self._gui.y_offset += 50
                    elif event.key == K_LEFT:
                        self._gui.x_offset -= 50
                    elif event.key == K_RIGHT:
                        self._gui.x_offset += 50
                    elif event.key == K_EQUALS:
                        self._gui.cell_size += 5
                    elif event.key == K_MINUS:
                        self._gui.cell_size -= 5
