from abc import ABC, abstractmethod

from src.events.event import Event


class EventHandler(ABC):
    # Interface of class that can handle events

    @abstractmethod
    def handle_events(self, events: list[Event]):
        pass
