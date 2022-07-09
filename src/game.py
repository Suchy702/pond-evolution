import pygame
from overrides import overrides

from src.constants import FPS
from src.engine import Engine
from src.events.event import Event, EventType, PygameEventType
from src.events.event_handler import EventHandler
from src.events.event_manager import EventManager
from src.graphics.gui import GUI
from src.simulation_settings import SimulationSettings


class Game(EventHandler):
    def __init__(self):
        pygame.init()

        self._settings = SimulationSettings()
        self._settings.pond_width = 200
        self._settings.pond_height = 200

        self._engine = Engine(self._settings)
        self._engine._interactor.preparations()
        self._gui = GUI(self._settings, self._engine.all_handlers)

        self._event_handler = EventManager()
        self._event_handler.add_handlers([self, self._engine, self._gui])

        self._running = True

    def run(self) -> None:
        clock = pygame.time.Clock()
        pygame.time.set_timer(PygameEventType.RUN_LOGIC, self._settings.logic_delay)

        while self._running:
            clock.tick(FPS)

            self._gui.draw_frame()
            self._event_handler.handle_events()

    @overrides
    def handle_events(self, events: list[Event]):
        for event in events:
            if event.event_type == EventType.QUIT:
                self._running = False
            elif event.event_type == EventType.RUN_LOGIC:
                self._engine.cycle()
            elif event.event_type == EventType.KEY_PRESSED:
                match event.args['key']:
                    case '.':
                        self._settings.logic_delay = max(100, self._settings.logic_delay - 10)
                        self._update_timer()
                    case ',':
                        self._settings.logic_delay = min(2000, self._settings.logic_delay + 10)
                        self._update_timer()

    def _update_timer(self):
        pygame.time.set_timer(PygameEventType.RUN_LOGIC, 0)
        pygame.time.set_timer(PygameEventType.RUN_LOGIC, self._settings.logic_delay)
