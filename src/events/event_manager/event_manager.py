from abc import ABC, abstractmethod

from src.events.event import Event


class EventManager(ABC):
    @abstractmethod
    def handle_events(self) -> None:
        pass

    @abstractmethod
    def add_event(self, event: Event) -> None:
        pass

    def add_events(self, events: list[Event]) -> None:
        for event in events:
            self.add_event(event)

    @abstractmethod
    def clear(self) -> None:
        pass
