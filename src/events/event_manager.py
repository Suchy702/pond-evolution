import pygame

from src.events.event import Event
from src.events.event_handler import EventHandler
from src.singleton import Singleton


class EventManager(metaclass=Singleton):
    def __init__(self):
        self._events: list[Event] = []
        self._animation_events: list[Event] = []
        self._handlers: list[EventHandler] = []

    def add_handlers(self, handlers: list[EventHandler]):
        self._handlers.extend(handlers)

    def emit_event(self, event: Event) -> None:
        if event.type.name.startswith("ANIM_"):
            self._animation_events.append(event)
        else:
            self._events.append(event)

    @staticmethod
    def _get_events_from_pygame() -> list[Event]:
        events = []
        for event in pygame.event.get():
            converted = Event.from_pygame_event(event)
            if converted is not None:
                events.append(converted)

        events.extend(Event.from_pygame_pressed_keys_dict(pygame.key.get_pressed()))
        return events

    def handle_events(self) -> None:
        self._events.extend(self._get_events_from_pygame())
        cp_events = self._events.copy()
        cp_anim_events = self._animation_events.copy()

        for handler in self._handlers:
            handler.handle_events(cp_events)
            handler.handle_animation_events(cp_anim_events)

        # Delete old events. During previous loop some events might have been emitted. We need to make sure not to
        # delete them.
        n_events = []
        cp_events_set = set(cp_events)
        for event in self._events:
            if event not in cp_events_set:
                n_events.append(event)

        n_anim_events = []
        cp_anim_events_set = set(cp_anim_events)
        for event in self._animation_events:
            if event not in cp_anim_events_set:
                n_anim_events.append(event)

        self._events = n_events
        self._animation_events = n_anim_events

    def is_animation_event(self):
        return len(self._animation_events) != 0
