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
        self._engine.prepare()

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

    def _user_close_program(self):
        return self._settings.screen_height is None

    def _end_game_actions(self) -> None:
        self._gui.hide_screen()
        self._statistics.show_statistics()

    def _skipped_game(self) -> None:
        self._event_emitter.clear_gui_events()
        self._event_emitter.handle_events()
        self._engine.cycle()
        self._statistics.make_snapshot()
        self.skip -= 1

    def _normal_game(self) -> None:
        if self._gui.is_animation_finished():
            self._engine.cycle()
            self._statistics.make_snapshot()

        self._event_emitter.handle_events()

    def _game_type_decision(self) -> None:
        if self.skip:
            self._skipped_game()
        else:
            self._normal_game()

    def run(self) -> None:
        clock = pygame.time.Clock()
        while self.running:
            clock.tick(FPS)
            self._game_type_decision()
        self._end_game_actions()
