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
    QUIT
)


@unique
class EventType(Enum):
    KEY_PRESSED = auto()
    QUIT = auto()
    OPEN_ADD_FISH_TOOLBOX = auto()

    def __str__(self):
        return self.name


@dataclass
class Event:
    event_type: EventType
    args: dict[str, any]

    def __init__(self, event_type: EventType, **args):
        self.event_type = event_type
        self.args = args

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
            events.append(Event(EventType.KEY_PRESSED, key="equals"))
        if keys[K_MINUS]:
            events.append(Event(EventType.KEY_PRESSED, key="minus"))

        return events
