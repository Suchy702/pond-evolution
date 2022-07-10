from overrides import overrides

from src.events.event import GameEvent
from src.events.event_manager.event_manager import EventManager
from src.events.event_type import GameEventType
from src.game import Game


class GameEventManager(EventManager):
    def __init__(self, game: Game):
        self._events: list[GameEvent] = []
        self._game: Game = game

    @overrides
    def add_event(self, event: GameEvent) -> None:
        self._events.append(event)

    def handle_events(self) -> None:
        cp_events = self._events.copy()

        for event in self._events:
            self._handle_event(event)

        # Delete old events. During previous loop some events might have been emitted. We need to make sure not to
        # delete them.
        n_events = []
        cp_events_set = set(cp_events)
        for event in self._events:
            if event not in cp_events_set:
                n_events.append(event)

        self._events = n_events

    def _handle_event(self, event: GameEvent):
        if event.event_type.name == GameEventType.QUIT:
            self._game.running = False
