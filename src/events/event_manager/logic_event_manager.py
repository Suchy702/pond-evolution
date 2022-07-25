from typing import cast

from overrides import overrides

from src.events.event import LogicEvent, Event
from src.events.event_manager.event_manager import EventManager
from src.logic.engine import Engine


class LogicEventManager(EventManager):
    def __init__(self, engine: Engine):
        self._events: list[LogicEvent] = []
        self._handler: Engine = engine

    @overrides
    def add_event(self, event: Event) -> None:
        event = cast(LogicEvent, event)
        self._events.append(event)

    @overrides
    def handle_events(self) -> None:
        pass
