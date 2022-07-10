from __future__ import annotations

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


class Event:
    def __init__(self, event_type: EventType, **args):
        self.type: EventType = event_type
        self.args: dict[str, any] = args

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
        supported_keys = [K_UP, K_DOWN, K_LEFT, K_RIGHT, K_EQUALS, K_MINUS, K_c, K_COMMA, K_PERIOD]
        transformed_keys = ['up', 'down', 'left', 'right', '=', '-', 'c', ',', '.']

        for idx, supported_key in enumerate(supported_keys):
            if keys[supported_key]:
                events.append(Event(EventType.KEY_PRESSED, key=transformed_keys[idx]))

        return events
