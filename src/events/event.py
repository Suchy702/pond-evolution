from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto, unique

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_MINUS,
    K_EQUALS,
    K_c,
    K_COMMA,
    K_PERIOD,
    QUIT
)


@unique
class EventType(Enum):
    # LOGICAL
    KEY_PRESSED = auto()
    RUN_LOGIC = auto()
    QUIT = auto()

    # ANIMATION
    ANIM_MOVE = auto()
    ANIM_STAY = auto()

    def __str__(self):
        return self.name


@dataclass
class Event:
    type: EventType
    args: dict[str, any]

    def __init__(self, event_type: EventType, **args):
        self.type = event_type
        self.args = args

    def copy(self) -> Event:
        return Event(self.type, **self.args)

    @staticmethod
    def from_pygame_event(event) -> Event | None:
        if event.type == QUIT:
            return Event(EventType.QUIT)
        return None

    @staticmethod
    def from_pygame_pressed_keys_dict(keys) -> list[Event]:
        events = []
        if keys[K_UP]:
            events.append(Event(EventType.KEY_PRESSED, key="up"))
        if keys[K_DOWN]:
            events.append(Event(EventType.KEY_PRESSED, key="down"))
        if keys[K_LEFT]:
            events.append(Event(EventType.KEY_PRESSED, key="left"))
        if keys[K_RIGHT]:
            events.append(Event(EventType.KEY_PRESSED, key="right"))
        if keys[K_EQUALS]:
            events.append(Event(EventType.KEY_PRESSED, key="="))
        if keys[K_MINUS]:
            events.append(Event(EventType.KEY_PRESSED, key="-"))
        if keys[K_c]:
            events.append(Event(EventType.KEY_PRESSED, key="c"))
        if keys[K_COMMA]:
            events.append(Event(EventType.KEY_PRESSED, key=","))
        if keys[K_PERIOD]:
            events.append(Event(EventType.KEY_PRESSED, key="."))

        return events
