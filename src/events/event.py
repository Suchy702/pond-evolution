from __future__ import annotations

from abc import abstractmethod, ABC
from typing import Optional

from overrides import overrides

from src.events.event_type import LogicEventType, GraphicEventType
from src.object.pond_object import PondObject


class Event(ABC):
    # TODO: jakoś zaimplementować łatwiej
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
                 to_y: Optional[int] = None,
                 step: Optional[int] = 1,
                 total_steps: Optional[int] = None):
        self.event_type = event_type
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
        return GraphicEvent(self.event_type, key=self.key, pond_object=self.pond_object, x=self.x, y=self.y,
                            from_x=self.from_x, from_y=self.from_y, to_x=self.to_x, to_y=self.to_y, step=self.step,
                            total_steps=self.total_steps)


class GameEvent(Event):
    def __init__(self, event_type: LogicEventType):
        self.event_type = event_type
