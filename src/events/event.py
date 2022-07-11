from __future__ import annotations

import inspect
from abc import ABC
from typing import Optional, TypeVar, Generic, cast

from overrides import overrides

from src.events.event_type import LogicEventType, GraphicEventType, EventType, GameEventType
from src.object.pond_object import PondObject

T = TypeVar('T', bound=EventType)


class Event(ABC, Generic[T]):
    def __init__(self, event_type: T, **kwargs):
        self.event_type: T = event_type

    def copy(self) -> Event:
        attributes = inspect.getmembers(self, lambda a: not (inspect.isroutine(a)))
        attributes = [a for a in attributes if not (a[0].startswith('_') or a[0].endswith('_'))]
        attr_set = {attr[0]: getattr(self, attr[0]) for attr in attributes}
        event_type = attr_set['event_type']
        attr_set.pop('event_type')
        return self.__class__(event_type, **attr_set)


class LogicEvent(Event[LogicEventType]):
    def __init__(self, event_type: LogicEventType):
        super().__init__(event_type)

    @overrides
    def copy(self) -> LogicEvent:
        cp = cast(LogicEvent, super().copy())
        return cp


class GraphicEvent(Event[GraphicEventType]):
    def __init__(self,
                 event_type: GraphicEventType, *,
                 key: Optional[str] = None,
                 pond_object: Optional[PondObject] = None,
                 x: Optional[int] = None,
                 y: Optional[int] = None,
                 from_x: Optional[int] = None,
                 from_y: Optional[int] = None,
                 to_x: Optional[int] = None,
                 to_y: Optional[int] = None,
                 step: Optional[int] = 1,
                 total_steps: Optional[int] = None):
        super().__init__(event_type)
        self.key = key
        self.pond_object = pond_object
        self.x = x
        self.y = y
        self.from_x = from_x
        self.from_y = from_y
        self.to_x = to_x
        self.to_y = to_y
        self.step: int = step
        self.total_steps: Optional[int] = total_steps

    @overrides
    def copy(self) -> GraphicEvent:
        cp = cast(GraphicEvent, super().copy())
        return cp

    def __str__(self):
        return self.event_type.name


class GameEvent(Event[GameEventType]):
    def __init__(self, event_type: GameEventType):
        super().__init__(event_type)

    @overrides
    def copy(self) -> GameEvent:
        cp = cast(GameEvent, super().copy())
        return cp
