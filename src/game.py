import pygame

from src.engine import Engine
from src.gui import GUI
from src.simulation_settings import SimulationSettings


class Game:
    def __init__(self):
        pass

    def run(self) -> None:
        settings = SimulationSettings()
        settings.pond_width = 10
        settings.pond_height = 10

        engine = Engine(settings)
        engine.preparations()
        engine.show_pond()

        gui = GUI(settings, [])
        cnt = 0

        while True:
            gui.draw_frame()
            cnt += 1
            if cnt == 10000:
                pygame.quit()
