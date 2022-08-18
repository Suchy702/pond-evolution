import pygame
import sys

from src.constants import FPS
from src.events.event_emitter import EventEmitter
from src.graphics.gui import GUI
from src.logic.engine import Engine
from src.simulation_settings import SimulationSettings
from src.statistics import Statistics


class Game:
    def __init__(self):
        pygame.init()

        self._settings = SimulationSettings()
        self._settings.get_user_settings()

        if self._user_close_program():
            sys.exit()

        self._engine = Engine(self._settings)
        self._gui = GUI(self._settings, self._engine)
        self._statistics = Statistics(self._settings, self._engine)

        self._event_emitter = EventEmitter()
        self._event_emitter.setup(self)

        self.running: bool = True
        self.skip: int = 0

    @property
    def gui(self) -> GUI:
        return self._gui

    @property
    def engine(self) -> Engine:
        return self._engine

    def run(self) -> None:
        clock = pygame.time.Clock()

        while self.running:
            clock.tick(FPS)
            self._choose_state()

        self._teardown()

    def _user_close_program(self):
        return not self._settings.finished_setup

    def _choose_state(self) -> None:
        if self.skip:
            self._skipped_state()
        else:
            self._normal_state()

    def _normal_state(self) -> None:
        if self._gui.is_animation_finished():
            self._engine.cycle()
            self._statistics.make_snapshot()

        self._event_emitter.handle_events()

    def _skipped_state(self) -> None:
        self._event_emitter.clear_gui_events()
        self._event_emitter.handle_events()
        self._engine.cycle()
        self._statistics.make_snapshot()
        self.skip -= 1

    def _teardown(self) -> None:
        self._gui.hide_screen()
        self._statistics.show_statistics()
