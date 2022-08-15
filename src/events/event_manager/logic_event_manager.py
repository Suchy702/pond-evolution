from __future__ import annotations

from typing import cast, TYPE_CHECKING

from overrides import overrides

from src.events.event_manager.event_manager import EventManager
from src.events.event import LogicEvent, Event
from src.events.event_type import LogicEventType

if TYPE_CHECKING:
    from src.logic.engine import Engine


class LogicEventManager(EventManager):
    def __init__(self, engine: Engine):
        self._events: list[LogicEvent] = []
        self._engine: Engine = engine

    @overrides
    def add_event(self, event: Event) -> None:
        event = cast(LogicEvent, event)
        self._events.append(event)

    def _handle_add_event(self, event: LogicEvent) -> None:
        self._engine.add_obj_by_click(event)

    @overrides
    def handle_events(self) -> None:
        cp_events = self._events.copy()
        self._events.clear()

        for event in cp_events:
            if event.event_type == LogicEventType.ADD:
                self._handle_add_event(event)

    @overrides
    def clear(self) -> None:
        self._events.clear()
