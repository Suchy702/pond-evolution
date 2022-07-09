import pygame
from overrides import overrides

from src.constants import FPS
from src.engine import Engine
from src.events.event import Event, EventType
from src.events.event_handler import EventHandler
from src.events.event_manager import EventManager
from src.graphics.gui import GUI
from src.simulation_settings import SimulationSettings


class Game(EventHandler):
    def __init__(self):
        pygame.init()

        self._settings = SimulationSettings()
        self._settings.pond_width = 15
        self._settings.pond_height = 15

        self._engine = Engine(self._settings)
        self._engine._interactor.preparations()
        self._gui = GUI(self._settings, self._engine.all_handlers)

        self._event_handler = EventManager()
        self._event_handler.add_handlers([self, self._engine, self._gui])

        self._running = True

    def run(self) -> None:
        clock = pygame.time.Clock()

        while self._running:
            clock.tick(FPS)

            if self._gui.is_animation_finished():
                self._engine.cycle()

            self._gui.draw_frame()
            self._event_handler.handle_events()

    @overrides
    def handle_events(self, events: list[Event]):
        for event in events:
            if event.event_type == EventType.QUIT:
                self._running = False
            elif event.event_type == EventType.RUN_LOGIC:
                self._engine.cycle()