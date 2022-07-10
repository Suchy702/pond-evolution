from overrides import overrides

from src.events.event import GameEvent
from src.events.event_manager.event_manager import EventManager
from src.graphics.gui import GUI


class GraphicEventManager(EventManager):
    def __init__(self, gui: GUI):
        self._events: list[GameEvent] = []
        self._animation_events: list[GameEvent] = []
        self._gui: GUI = gui

    @overrides
    def add_event(self, event: GameEvent) -> None:
        if event.event_type.name.startswith("ANIM_"):
            self._animation_events.append(event)
        else:
            self._events.append(event)

    def handle_events(self) -> None:
        cp_events = self._events.copy()
        cp_anim_events = self._animation_events.copy()

        for event in self._events:
            self._handle_static_event(event)
        for event in self._animation_events:
            self._handle_animation_event(event)

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

    def _handle_static_event(self, event: GameEvent):
        pass

    def _handle_animation_event(self, event: GameEvent):
        pass
