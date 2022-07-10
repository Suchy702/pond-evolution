from __future__ import annotations

from abc import abstractmethod, ABC
from typing import Optional

from src.events.event_type import LogicEventType, GraphicEventType
from src.object.pond_object import PondObject


class Event(ABC):
    # TODO: jakoś zaimplementować
    @abstractmethod
    def copy(self) -> Event:
        pass


class LogicEvent(Event):
    def __init__(self, event_type: LogicEventType):
        self.event_type: LogicEventType = event_type


class GraphicEvent(Event):
    def __init__(self,
                 event_type: GraphicEventType, *,
                 key: Optional[str] = None,
                 pond_object: Optional[PondObject] = None,
                 x: Optional[int] = None,
                 y: Optional[int] = None,
                 from_x: Optional[int] = None,
                 from_y: Optional[int] = None,
                 to_x: Optional[int] = None,
                 to_y: Optional[int] = None):
        self.event_type = event_type
        self.key = key
        self.pond_object = pond_object
        self.x = x
        self.y = y
        self.from_x = from_x
        self.from_y = from_y
        self.to_x = to_x
        self.to_y = to_y


class GameEvent(Event):
    def __init__(self, event_type: LogicEventType):
        self.event_type = event_type
