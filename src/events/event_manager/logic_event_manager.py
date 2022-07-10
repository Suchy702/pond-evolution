from typing import cast

from overrides import overrides

from src.engine import Engine
from src.events.event import LogicEvent, Event
from src.events.event_manager.event_manager import EventManager


class LogicEventManager(EventManager):
    def __init__(self, engine: Engine):
        self._events: list[LogicEvent] = []
        self._handler: Engine = engine

    @overrides
    def add_event(self, event: Event) -> None:
        event = cast(event, LogicEvent)
        self._events.append(event)

    @overrides
    def handle_events(self) -> None:
        pass
