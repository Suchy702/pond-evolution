from __future__ import annotations

from abc import ABC
from typing import Optional, TypeVar, Generic, cast

from overrides import overrides

from src.events.event_type import LogicEventType, GraphicEventType, EventType, GameEventType, ClickEventType
from src.object.pond_object import PondObject
from src.position import Position

T = TypeVar('T', bound=EventType)


class Event(ABC, Generic[T]):
    def __init__(self, event_type: T, **kwargs):
        self.event_type: T = event_type
        self.attributes: list[str] = ['event_type']

        self._get_attribute_names()

    def _get_attribute_names(self) -> None:
        for param in self.__init__.__code__.co_varnames[2:2 + self.__init__.__code__.co_kwonlyargcount]:  # type: ignore
            self.attributes.append(param)

    def copy(self) -> Event:
        kwargs = {}
        for attr in self.attributes:
            if attr == 'event_type':
                continue
            kwargs[attr] = getattr(self, attr)

        return self.__class__(self.event_type, **kwargs)


class LogicEvent(Event[LogicEventType]):
    def __init__(self, event_type: LogicEventType, obj: PondObject, pos: Position):
        super().__init__(event_type)
        self.obj = obj
        self.pos = pos

    @overrides
    def copy(self) -> LogicEvent:
        cp = cast(LogicEvent, super().copy())
        return cp

    def __str__(self):
        return f'LogicEvent({self.event_type.name})'


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
                 total_steps: Optional[int] = None,
                 is_flipped: Optional[bool] = None,
                 rotate: Optional[float] = None):
        super().__init__(event_type)
        self.key = key
        self.pond_object = pond_object
        self.x = x
        self.y = y
        self.from_x = from_x
        self.from_y = from_y
        self.to_x = to_x
        self.to_y = to_y
        self.step = step
        self.total_steps = total_steps
        self.is_flipped = is_flipped
        self.rotate = rotate

    @overrides
    def copy(self) -> GraphicEvent:
        cp = cast(GraphicEvent, super().copy())
        return cp

    def should_make_next_step(self) -> bool:
        return self.step < self.total_steps

    def __str__(self):
        return f'GraphicEvent({self.event_type.name})'


class GameEvent(Event[GameEventType]):
    def __init__(self, event_type: GameEventType):
        super().__init__(event_type)

    @overrides
    def copy(self) -> GameEvent:
        cp = cast(GameEvent, super().copy())
        return cp

    def __str__(self):
        return f'GameEvent({self.event_type.name})'


class ClickEvent(Event[ClickEventType]):
    def __init__(self, event_type: ClickEventType, pos: tuple[int, int]):
        super().__init__(event_type)
        self.pos: tuple[int, int] = pos

    def __str__(self):
        return f'ClickEvent({self.event_type.name})'
