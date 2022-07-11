from __future__ import annotations

from typing import TYPE_CHECKING

from overrides import overrides

from src.events.event import GameEvent, Event
from src.events.event_manager.event_manager import EventManager
from src.events.event_type import GameEventType

if TYPE_CHECKING:
    from src.game import Game


class GameEventManager(EventManager):
    def __init__(self, game: Game):
        self._events: list[GameEvent] = []
        self._game: Game = game

    @overrides
    def add_event(self, event: Event) -> None:
        self._events.append(event)

    def handle_events(self) -> None:
        cp_events = self._events.copy()
        self._events.clear()

        for event in cp_events:
            self._handle_event(event)

    def _handle_event(self, event: GameEvent):
        if event.event_type == GameEventType.QUIT:
            self._game.running = False
