from typing import cast

from overrides import overrides

from src.events.event_manager.event_manager import EventManager
from src.events.event import Event, ClickEvent
from src.events.event_type import ClickEventType
from src.graphics.gui import GUI


class ClickingEventManager(EventManager):
    def __init__(self, gui: GUI):
        self._add_events = []
        self._check_events = []

        self._gui = gui

    @overrides
    def add_event(self, event: Event) -> None:
        event = cast(ClickEvent, event)
        if event.event_type == ClickEventType.ADDING:
            self._add_events.append(event)
        else:
            self._check_events.append(event)

    def _handle_add_event(self, event: ClickEvent) -> None:
        click_coor = self._gui.get_click_coor(event.pos)


    def _handle_add_events(self) -> None:
        cp_events = self._add_events.copy()
        self._add_events.clear()

        for event in cp_events:
            self._handle_add_event(event)

    def _handle_check_event(self, event: ClickEvent) -> None:
        pass

    def _handle_check_events(self) -> None:
        cp_events = self._check_events.copy()
        self._check_events.clear()

        for event in cp_events:
            self._handle_check_event(event)

    @overrides
    def handle_events(self) -> None:
        self._handle_add_events()
        self._handle_check_events()
