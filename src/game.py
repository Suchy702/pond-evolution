import pygame

from src.constants import FPS
from src.engine import Engine
from src.events.event_emitter import EventEmitter
from src.events.event_manager.game_event_manager import GameEventManager
from src.events.event_manager.graphic_event_manager import GraphicEventManager
from src.events.event_manager.logic_event_manager import LogicEventManager
from src.graphics.gui import GUI
from src.simulation_settings import SimulationSettings


class Game:
    def __init__(self):
        pygame.init()

        self._settings = SimulationSettings()

        self._engine = Engine(self._settings)
        self._engine.demo()
        self._gui = GUI(self._settings)

        self._event_emitter = EventEmitter()
        self._game_event_manager = GameEventManager(self)
        self._graphic_event_manager = GraphicEventManager(self._gui)
        self._logic_event_manager = LogicEventManager(self._engine)
        self._event_emitter.game_event_manager = self._game_event_manager
        self._event_emitter.graphic_event_manager = self._graphic_event_manager
        self._event_emitter.logic_event_manager = self._logic_event_manager

        self.running = True

    def run(self) -> None:
        clock = pygame.time.Clock()
        self._gui.draw_empty_frame()
        pygame.display.update()

        while self.running:
            clock.tick(FPS)

            if self._gui.is_animation_finished():
                self._engine.cycle()

            self._event_emitter.handle_events()
