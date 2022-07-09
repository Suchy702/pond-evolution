from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto, unique, IntEnum

import pygame
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


class PygameEventType(IntEnum):
    def _generate_next_value_(name, start, count, last_values):
        return pygame.USEREVENT + count + 1

    RUN_LOGIC = auto()

    def __str__(self):
        return self.name


@unique
class EventType(Enum):
    KEY_PRESSED = auto()
    QUIT = auto()
    RUN_LOGIC = auto()

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
        elif event.type == PygameEventType.RUN_LOGIC:
            return Event(EventType.RUN_LOGIC)
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
